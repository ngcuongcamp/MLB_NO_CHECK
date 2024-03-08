from libs.libs import QThread, pyqtSignal, cv2, np
from utilities import config, logger


#! Camera Class


class CameraThread(QThread):
    frame_received = pyqtSignal(np.ndarray)
    update_error_signal = pyqtSignal()

    def __init__(self, camera_id):

        super(CameraThread, self).__init__()
        self.camera_id = camera_id
        self.is_running = True
        self.cap = cv2.VideoCapture(self.camera_id, cv2.CAP_DSHOW)
        # self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1281)
        # self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1025)
        # PROP_EXPOSURE = int(config["SETTING"]["PROP_EXPOSURE"])
        # self.cap.set(cv2.CAP_PROP_EXPOSURE, PROP_EXPOSURE)

    def run(self):
        is_alert_error = False
        while self.is_running:
            self.ret, self.frame = self.cap.read()
            if not self.ret:
                if not is_alert_error:
                    is_alert_error = True
                    self.update_error_signal.emit()
                    self.cap.release()
                    logger.error("Camera Error")
                    self.is_running = False
            else:
                is_alert_error = False
                self.frame_received.emit(self.frame)
            cv2.waitKey(1)

    def stop(self):
        self.is_running = False
        self.requestInterruption()
        self.cap.release()
        self.quit()
