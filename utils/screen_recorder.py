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

    ALLURE_AVAILABLE = True
except ImportError:
    ALLURE_AVAILABLE = False
    allure = None


def _even(x: int) -> int:
    """Juft sonni qaytaradi (video codec talabi)"""
    return int(x) // 2 * 2


def _sanitize(name: str) -> str:
    """Fayl nomidagi noto'g'ri belgilarni tozalash"""
    return re.sub(r'[<>:"/\\|?*]+', "_", name)


class ScreenRecorder:
    """
    Selenium WebDriver orqali brauzer skrinshotlaridan video yozish.

    Features:
    - FFmpeg bilan yuqori sifatli H.264 MP4 yoki VP9 WebM
    - FFmpeg bo'lmasa OpenCV fallback
    - Async screenshot recording
    - Allure integratsiyasi
    - Overlay matn (vaqt, test nomi, URL)
    - Minimal logging (faqat muhim xabarlar)
    """

    def __init__(
            self,
            driver,
            filename: str = "{test}_{ts}.mp4",
            output_dir: str = "artifacts/videos",
            fps: float = 10.0,
            size="auto",
            prefer: str = "h264",
            draw_info: bool = False,
            info_supplier=None,
            attach_to_allure: bool = True,
            keep_on_success: bool = True,
            test_name: str | None = None
    ):
        if not RECORDING_AVAILABLE:
            raise ImportError(
                "ScreenRecorder requires opencv-python and numpy.\n"
                "Install: pip install opencv-python numpy"
            )

        self.driver = driver
        self.fps = float(fps)
        self.size = size
        self.prefer = prefer.lower()
        self.draw_info = draw_info
        self.info_supplier = info_supplier
        self.attach_to_allure = attach_to_allure and ALLURE_AVAILABLE
        self.keep_on_success = keep_on_success

        self.test_name = test_name or "test"

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.filename = _sanitize(filename.format(test=self.test_name, ts=ts))
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.filepath = os.path.join(self.output_dir, self.filename)

        # Internal state
        self._writer = None
        self._ff = None
        self._w = self._h = None
        self._thread = None
        self._stop = threading.Event()
        self._frame_count = 0
        self._error_count = 0
        self._max_errors = 10

        # Flags to prevent repeated warnings
        self._ffmpeg_warned = False
        self._writer_initialized = False

        # Logging
        self._log = logging.getLogger(self.__class__.__name__)
        if not self._log.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - [%(levelname)s] - %(name)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self._log.addHandler(handler)
            self._log.setLevel(logging.INFO)

    # ==================== Public API ====================

    def start(self):
        """Video yozuvni boshlash"""
        if self._thread and self._thread.is_alive():
            self._log.warning("ScreenRecorder allaqachon ishga tushgan.")
            return

        self._stop.clear()
        self._frame_count = 0
        self._error_count = 0

        self._thread = threading.Thread(
            target=self._loop,
            name=f"ScreenRecorder-{self.test_name}",
            daemon=True
        )
        self._thread.start()
        self._log.info(f"🎥 Recording started → {self.filepath}")

    def stop(self):
        """Video yozuvni to'xtatish"""
        if not self._thread or not self._thread.is_alive():
            self._log.warning("ScreenRecorder ishlamayapti.")
            return

        self._log.info("⏹️  Stopping recording...")
        self._stop.set()

        if self._thread:
            self._thread.join(timeout=10)
            if self._thread.is_alive():
                self._log.error("Thread to'xtatilmadi!")

        self._close_writers()

        # Statistika
        if self._frame_count > 0:
            duration = self._frame_count / self.fps
            size_mb = os.path.getsize(self.filepath) / (1024 * 1024) if os.path.exists(self.filepath) else 0
            self._log.info(
                f"🎬 Recording completed: {self._frame_count} frames, "
                f"{duration:.1f}s, {size_mb:.2f} MB"
            )

        if self.attach_to_allure and os.path.exists(self.filepath):
            self._attach_to_allure()

    # ==================== Internals ====================

    def _close_writers(self):
        """FFmpeg va OpenCV writers ni yopish"""
        if self._ff:
            try:
                self._ff.stdin.close()
                self._ff.wait(timeout=10)
            except Exception as e:
                self._log.debug(f"FFmpeg close xatosi: {e}")
            finally:
                self._ff = None

        if self._writer:
            try:
                self._writer.release()
            except Exception as e:
                self._log.debug(f"OpenCV release xatosi: {e}")
            finally:
                self._writer = None

    def _attach_to_allure(self):
        """Video faylni Allure reportga biriktirish"""
        if not ALLURE_AVAILABLE:
            return

        try:
            ext = os.path.splitext(self.filepath)[1].lower()

            if ext == ".mp4":
                mime = allure.attachment_type.MP4
            elif ext == ".webm":
                mime = allure.attachment_type.WEBM
            else:
                mime = "video/mp4"

            allure.attach.file(
                self.filepath,
                name=os.path.basename(self.filepath),
                attachment_type=mime,
                extension=ext
            )
            self._log.info(f"📎 Video attached to Allure report")
        except Exception as e:
            self._log.warning(f"Allure attach xatosi: {e}")

    def _open_ffmpeg(self):
        """FFmpeg pipe orqali video yozish"""
        if shutil.which("ffmpeg") is None:
            if not self._ffmpeg_warned:
                self._log.warning(
                    "⚠️  FFmpeg topilmadi. OpenCV fallback ishlatiladi (mp4v codec). "
                    "Yaxshiroq sifat uchun FFmpeg o'rnating: https://ffmpeg.org"
                )
                self._ffmpeg_warned = True
            return None

        ext = os.path.splitext(self.filepath)[1].lower()
        w, h = self._w, self._h

        if self.prefer == "vp9" or ext == ".webm":
            if ext != ".webm":
                self.filepath = os.path.splitext(self.filepath)[0] + ".webm"

            cmd = [
                "ffmpeg", "-y",
                "-f", "rawvideo", "-pix_fmt", "bgr24",
                "-s", f"{w}x{h}", "-r", str(self.fps),
                "-i", "-",
                "-c:v", "libvpx-vp9",
                "-b:v", "1M",
                "-deadline", "realtime",
                "-cpu-used", "4",
                self.filepath
            ]
        else:
            if ext != ".mp4":
                self.filepath = os.path.splitext(self.filepath)[0] + ".mp4"

            cmd = [
                "ffmpeg", "-y",
                "-f", "rawvideo", "-pix_fmt", "bgr24",
                "-s", f"{w}x{h}", "-r", str(self.fps),
                "-i", "-",
                "-c:v", "libx264",
                "-preset", "ultrafast",
                "-pix_fmt", "yuv420p",
                "-movflags", "+faststart",
                self.filepath
            ]

        try:
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            self._log.info(f"✅ FFmpeg encoder: {self.prefer.upper()}")
            return process
        except Exception as e:
            if not self._ffmpeg_warned:
                self._log.warning(f"FFmpeg start xatosi: {e}")
                self._ffmpeg_warned = True
            return None

    def _open_opencv(self):
        """OpenCV VideoWriter fallback"""
        ext = os.path.splitext(self.filepath)[1].lower()
        if ext != ".mp4":
            self.filepath = os.path.splitext(self.filepath)[0] + ".mp4"

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        writer = cv2.VideoWriter(
            self.filepath,
            fourcc,
            self.fps,
            (self._w, self._h)
        )

        if not writer.isOpened():
            raise RuntimeError(f"OpenCV VideoWriter ochilmadi: {self.filepath}")

        return writer

    def _ensure_sinks(self, frame_bgr):
        """Video writer ni yaratish (birinchi frame kelganda)"""
        if self._writer_initialized:
            return

        if self._w is None or self._h is None:
            h, w = frame_bgr.shape[:2]

            if isinstance(self.size, (tuple, list)) and len(self.size) == 2:
                w, h = map(int, self.size)

            self._w, self._h = _even(w), _even(h)
            self._log.info(f"📹 Video: {self._w}x{self._h} @ {self.fps} FPS")

        # FFmpeg first (faqat bir marta urinadi)
        if self.prefer in ("h264", "vp9"):
            self._ff = self._open_ffmpeg()

        # OpenCV fallback (agar FFmpeg bo'lmasa)
        if self._ff is None:
            self._writer = self._open_opencv()

        self._writer_initialized = True

    def _overlay(self, frame_bgr):
        """Video frame'ga matn yozish"""
        if not self.draw_info:
            return frame_bgr

        h, w = frame_bgr.shape[:2]
        now = datetime.now().strftime('%H:%M:%S')

        try:
            url = self.driver.current_url
        except Exception:
            url = ""

        lines = [
            f"Time: {now}",
            f"Test: {self.test_name}",
            f"URL: {url}"
        ]

        if callable(self.info_supplier):
            try:
                extra = str(self.info_supplier()) or ""
                if extra:
                    lines.append(extra)
            except Exception:
                pass

        y = 24
        for txt in lines:
            # Shadow
            cv2.putText(
                frame_bgr, txt, (10, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (0, 0, 0), 3, cv2.LINE_AA
            )
            # Main text
            cv2.putText(
                frame_bgr, txt, (10, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (255, 255, 255), 1, cv2.LINE_AA
            )
            y += 20

        return frame_bgr

    def _write_frame(self, frame_bgr):
        """Frame'ni video faylga yozish"""
        # Resize
        if frame_bgr.shape[1] != self._w or frame_bgr.shape[0] != self._h:
            frame_bgr = cv2.resize(frame_bgr, (self._w, self._h))

        frame_bgr = self._overlay(frame_bgr)

        # FFmpeg
        if self._ff is not None:
            try:
                self._ff.stdin.write(frame_bgr.tobytes())
                self._frame_count += 1
                return
            except Exception as e:
                self._log.debug(f"FFmpeg write xatosi: {e}")
                self._ff = None
                if self._writer is None:
                    self._writer = self._open_opencv()

        # OpenCV
        if self._writer is not None:
            try:
                self._writer.write(frame_bgr)
                self._frame_count += 1
            except Exception as e:
                self._log.error(f"OpenCV write xatosi: {e}")
                self._error_count += 1

    def _loop(self):
        """Asosiy screenshot olish va yozish loop"""
        delay = max(1.0 / self.fps, 0.001)

        while not self._stop.is_set():
            t0 = time.time()

            try:
                png = self.driver.get_screenshot_as_png()
                if not png:
                    time.sleep(delay)
                    continue

                frame = cv2.imdecode(
                    np.frombuffer(png, np.uint8),
                    cv2.IMREAD_COLOR
                )

                if frame is None:
                    self._log.debug("Frame decode xatosi")
                    time.sleep(delay)
                    continue

                # Writers yaratish (faqat birinchi marta)
                self._ensure_sinks(frame)

                # Yozish
                self._write_frame(frame)

            except Exception as e:
                self._log.debug(f"Loop xatosi: {e}")
                self._error_count += 1

                if self._error_count > self._max_errors:
                    self._log.error(
                        f"Juda ko'p xato ({self._error_count}), to'xtatilmoqda"
                    )
                    break

            # FPS timing
            dt = time.time() - t0
            if dt < delay:
                time.sleep(delay - dt)

        self._log.debug("Recording loop tugadi")