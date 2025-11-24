import os, re, time, threading, logging, shutil, subprocess
from datetime import datetime

try:
    import cv2
    import numpy as np
    RECORDING_AVAILABLE = True
except ImportError:
    RECORDING_AVAILABLE = False
    cv2 = None
    np = None

try:
    import allure
except Exception:
    allure = None

def _even(x: int) -> int:
    return int(x) // 2 * 2

def _sanitize(name: str) -> str:
    return re.sub(r'[<>:"/\\|?*]+', "_", name)


class ScreenRecorder:
    """
    Brauzer skrinshotlaridan video yig'adi.
    - ffmpeg mavjud bo'lsa: H.264 MP4 (yoki WebM) — Allure/HTML5 uchun mos
    - ffmpeg yo'q bo'lsa: OpenCV ("mp4v") fallback
    """
    def __init__(
        self,
        driver,
        filename: str = "{test}_{ts}.mp4",   # .mp4 yoki .webm yozish mumkin
        output_dir: str = "artifacts/videos",
        fps: float = 8.0,
        size="auto",                         # "auto" yoki (w, h)
        prefer: str = "h264",                # "h264", "vp9", "opencv"
        draw_info: bool = False,             # overlay: vaqt/test/URL
        info_supplier=None,                  # qo'shimcha overlay matn
        attach_to_allure: bool = False,
        keep_on_success: bool = True,
        test_name: str | None = None
    ):
        self.driver = driver
        self.fps = float(fps)
        self.size = size
        self.prefer = prefer.lower()
        self.draw_info = draw_info
        self.info_supplier = info_supplier
        self.attach_to_allure = attach_to_allure
        self.keep_on_success = keep_on_success

        # test nomi (agar pytestdan berilsa)
        self.test_name = test_name or "test"

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.filename = _sanitize(filename.format(test=self.test_name, ts=ts))
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.filepath = os.path.join(self.output_dir, self.filename)

        self._writer = None          # OpenCV writer
        self._ff = None              # ffmpeg subprocess
        self._w = self._h = None
        self._thread = None
        self._stop = threading.Event()
        self._log = logging.getLogger(self.__class__.__name__)

    # ------------------------------ Public API ------------------------------

    def start(self):
        if self._thread and self._thread.is_alive():
            self._log.warning("ScreenRecorder allaqachon ishga tushgan.")
            return
        self._stop.clear()
        self._thread = threading.Thread(target=self._loop, name="ScreenRecorder", daemon=True)
        self._thread.start()
        self._log.info(f"🎥 Recording started → {self.filepath}")

    def stop(self):
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=5)
        # close writers
        if self._ff:
            try:
                self._ff.stdin.close()
            except Exception:
                pass
            self._ff.wait(timeout=10)
            self._ff = None
        if self._writer:
            try:
                self._writer.release()
            except Exception:
                pass
            self._writer = None

        # Allure attach
        if self.attach_to_allure and allure and os.path.exists(self.filepath):
            try:
                ext = os.path.splitext(self.filepath)[1].lower()
                mime = allure.attachment_type.MP4 if ext == ".mp4" else allure.attachment_type.WEBM
                allure.attach.file(self.filepath, name=os.path.basename(self.filepath), attachment_type=mime)
            except Exception:
                pass

        self._log.info("🎬 Recording stopped")

    # ------------------------------ Internals -------------------------------

    def _open_ffmpeg(self):
        """Start ffmpeg pipe if available & requested."""
        if shutil.which("ffmpeg") is None:
            return None

        ext = os.path.splitext(self.filepath)[1].lower()
        w, h = self._w, self._h

        if self.prefer == "vp9" or ext == ".webm":
            # WEBM (VP9) — brauzerlar juda yaxshi qo'llaydi
            cmd = [
                "ffmpeg", "-y",
                "-f", "rawvideo", "-pix_fmt", "bgr24",
                "-s", f"{w}x{h}", "-r", str(self.fps),
                "-i", "-",
                "-c:v", "libvpx-vp9", "-b:v", "1M",
                self.filepath
            ]
        else:
            # H.264 MP4 (default)
            # yuv420p + faststart — HTML5 mosligi va tez ochilish
            if ext != ".mp4":
                # foydalanuvchi .webm yozsa, prefer h264 bo'lsa avtomatik .mp4ga o'zgartiramiz
                self.filepath = os.path.splitext(self.filepath)[0] + ".mp4"
            cmd = [
                "ffmpeg", "-y",
                "-f", "rawvideo", "-pix_fmt", "bgr24",
                "-s", f"{w}x{h}", "-r", str(self.fps),
                "-i", "-",
                "-c:v", "libx264", "-preset", "veryfast",
                "-pix_fmt", "yuv420p",
                "-movflags", "+faststart",
                self.filepath
            ]

        self._log.info(f"ffmpeg cmd: {' '.join(cmd)}")
        try:
            return subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as e:
            self._log.warning(f"ffmpeg ishga tushmadi ({e}). OpenCV fallback ishlatiladi.")
            return None

    def _open_opencv(self):
        """OpenCV VideoWriter fallback (brauzerda har doim o‘qilmasligi mumkin)."""
        ext = os.path.splitext(self.filepath)[1].lower()
        if ext != ".mp4":
            self.filepath = os.path.splitext(self.filepath)[0] + ".mp4"

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        self._log.warning("OpenCV fallback: mp4v. Allure/HTML5 pleer buni har doim o‘qimaydi.")
        return cv2.VideoWriter(self.filepath, fourcc, self.fps, (self._w, self._h))

    def _ensure_sinks(self, frame_bgr):
        if self._w is None or self._h is None:
            h, w = frame_bgr.shape[:2]
            if isinstance(self.size, (tuple, list)) and len(self.size) == 2:
                w, h = map(int, self.size)
            self._w, self._h = _even(w), _even(h)

        # ffmpeg first
        if self._ff is None and (self.prefer in ("h264", "vp9")):
            self._ff = self._open_ffmpeg()

        # fallback
        if self._ff is None and self._writer is None:
            self._writer = self._open_opencv()

    def _overlay(self, frame_bgr):
        if not self.draw_info:
            return frame_bgr
        h, w = frame_bgr.shape[:2]
        now = datetime.now().strftime('%H:%M:%S')
        try:
            url = self.driver.current_url
        except Exception:
            url = ""
        lines = [now, self.test_name, url]
        if callable(self.info_supplier):
            try:
                extra = str(self.info_supplier()) or ""
                if extra:
                    lines.append(extra)
            except Exception:
                pass

        y = 24
        for txt in lines:
            cv2.putText(frame_bgr, txt, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 3, cv2.LINE_AA)
            cv2.putText(frame_bgr, txt, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
            y += 20
        return frame_bgr

    def _write_frame(self, frame_bgr):
        # resize to sink size
        if frame_bgr.shape[1] != self._w or frame_bgr.shape[0] != self._h:
            frame_bgr = cv2.resize(frame_bgr, (self._w, self._h))

        frame_bgr = self._overlay(frame_bgr)

        if self._ff is not None:
            try:
                self._ff.stdin.write(frame_bgr.tobytes())
                return
            except Exception:
                self._log.debug("ffmpeg write xatosi, OpenCV fallback'ga o'tamiz.")
                self._ff = None
                self._writer = self._open_opencv()

        # OpenCV fallback
        self._writer.write(frame_bgr)

    def _loop(self):
        delay = max(1.0 / self.fps, 0.001)
        while not self._stop.is_set():
            t0 = time.time()
            try:
                png = self.driver.get_screenshot_as_png()
                if not png:
                    time.sleep(delay)
                    continue
                frame = cv2.imdecode(np.frombuffer(png, np.uint8), cv2.IMREAD_COLOR)
                self._ensure_sinks(frame)
                self._write_frame(frame)
            except Exception as e:
                self._log.debug(f"Frame yozishda xato: {e}")

            dt = time.time() - t0
            if dt < delay:
                time.sleep(delay - dt)
