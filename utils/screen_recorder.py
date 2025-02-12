import time
import cv2
import numpy as np
import os
from datetime import datetime
from threading import Thread
import logging


class ScreenRecorder:
    def __init__(self, driver, filename=None, fps=5, screen_size=(1280, 720)):
        self.driver = driver
        self.fps = fps
        self.screen_size = screen_size

        # Logging sozlamalari
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        # Video fayl nomini yaratish
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.filename = filename or f"video_{timestamp}.mp4"

        # Video papkasini yaratish
        self.video_dir = "video_records"
        if not os.path.exists(self.video_dir):
            os.makedirs(self.video_dir)

        self.filepath = os.path.join(self.video_dir, self.filename)
        self.recording = False
        self.thread = None

        # Video yozish sozlamalari
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.out = cv2.VideoWriter(
            self.filepath,
            fourcc,
            float(self.fps),
            self.screen_size
        )
        self.logger.info(f"Video yozish uchun tayyorlandi: {self.filepath}")

    def start_recording(self):
        self.recording = True
        self.thread = Thread(target=self._record)
        self.thread.daemon = True
        self.thread.start()
        self.logger.info("Video yozish boshlandi")

    def stop_recording(self):
        self.recording = False
        if self.thread:
            self.thread.join(timeout=5)
        self.out.release()
        self.logger.info(f"Video yozish tugatildi: {self.filepath}")

    def _record(self):
        frame_delay = 1.0 / self.fps
        while self.recording:
            try:
                start_time = time.time()

                screenshot = self.driver.get_screenshot_as_png()
                image = cv2.imdecode(
                    np.frombuffer(screenshot, np.uint8),
                    cv2.IMREAD_COLOR
                )

                resized_image = cv2.resize(image, self.screen_size)
                self.out.write(resized_image)

                processing_time = time.time() - start_time
                if processing_time < frame_delay:
                    time.sleep(frame_delay - processing_time)

            except Exception as e:
                self.logger.error(f"Kadr yozishda xatolik: {str(e)}")
                continue
