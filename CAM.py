from libs.libs import *
from utilities import *
from Thread_PLC import PLCThread
from Thread_Camera import CameraThread
from connect_mes import *
from reader import *
from UI_handler import *
from detect_qty import *


class MyApplication(QMainWindow):
    frame1 = None
    data_scan1 = None
    graph = FilterGraph()
    thread_pool = QThreadPool()

    def __init__(self):
        super().__init__()
        self.is_update_cam_error = True
        self.is_processing = False
        self.state_ui = None
        initial_UI_MainWindow(self)  # initialize UI
        read_config(self)  # read config

        # thread CAMERA
        self.open_camera_thread()
        self.check_error_camera = QTimer()
        self.check_error_camera.timeout.connect(self.reconnect_camera_thread)
        self.check_error_camera.start(1000)

        get_name_mes_app(self)  # connect MES APP

        # thread PLC
        self.THREAD_PLC = PLCThread(
            self.COM_PLC, self.BAUDRATE_PLC, timeout=0.009, ref=self
        )
        self.THREAD_PLC.start()
        self.THREAD_PLC.data_received.connect(self.handle_signal_plc)

    def handle_click_update(self, event):
        req = QMessageBox.question(
            self,
            "Confirm Update",
            "Do you want to update latest version?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if req == QMessageBox.Yes:
            cmd_printer("INFO", "Handler update function here...")
            req3 = QMessageBox.warning(
                self, "Infomation", "Not found latest version!", QMessageBox.Cancel
            )
        else:
            cmd_printer("INFO", "Ignore update")

    # handle plc signal
    def handle_signal_plc(self, data):
        if self.THREAD_CAMERA_1.is_running:
            if data == b"1\x00":
            # if data == b"1":
                cmd_printer("INFO", "\n\n------ SCAN SIGNAL -------")
                logger.info("\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
                logger.info("--> Received scan signal from PLC")
                logger.info("--> ------ SCAN SIGNAL -------")
                try:
                    self.worker = Worker(self.scan_product_code)
                    MyApplication.thread_pool.start(self.worker)
                except Exception as E:
                    print(E)
            if data == b"2\x00":
            # if data == b"2":
                cmd_printer("WARNING", "---------------\nRESET")
                set_reset_state(self)
                self.set_default_variables()
                self.is_processing = False
                self.state_ui = None
        else:
            cmd_printer(
                "WARNING", f"Error: Received signal when the camera is not connected"
            )
            cmd_printer("WARNING", f"Signal PLC: {data}")

    def scan_product_code(self):
        # set_default_state(self)
        self.set_default_variables()
        i = 0
        stime = time.time()
        while i < self.SCAN_LIMIT:
            i = i + 1
            gray_frame = process_frame(frame=self.frame1)
            self.data_scan1 = read_dmt_zxingcpp(gray_frame)
            if self.data_scan1:
                break
            if self.data_scan1 is None:
                processed = process_frame(frame=self.frame1)
                self.data_scan1 = read_dmt_loop(self, processed)
                if self.data_scan1:
                    break
        cmd_printer("INFO", "--> RESULT SCAN")
        logger.info("--> RESULT SCAN")
        cmd_printer(
            "INFO", f"-----> spends {round(time.time() - stime,3)}s to read code"
        )

        # IF FAIL SCAN
        if self.data_scan1 is None:
            cmd_printer("ERROR", "FAILED")
            logger.error("FAILED")
            self.THREAD_PLC.send_signal_to_plc(b"2")
            self.is_processing = False
            if self.IS_SAVE_NG_IMAGE == 1:
                if self.data_scan1 is None:
                    image_filename = "image_NG/{}/{}.png".format(
                        get_current_date(), format_current_time()
                    )
                    cv2.imwrite(image_filename, self.frame1)

            logger.error("------FAIL SCAN-------")

            logger.error(f"Data SN: {self.data_scan1}")

            cmd_printer("ERROR", "------FAIL SCAN-------")
            cmd_printer("ERROR", f"Data SN: {self.data_scan1}")
            if self.state_ui == True or self.state_ui == None:
                set_fail_state(self)
                self.state_ui = False

        # IF PASS SCAN
        if self.data_scan1 is not None:
            cmd_printer("SUCCESS", "PASS SCAN")
            logger.info("PASS SCAN")
            cmd_printer("SUCCESS", f"Data SN: {self.data_scan1}")

            cmd_printer("INFO", "----------- SEND TO SFC -----------")
            logger.info("----------- SEND TO SFC -----------")

            # PUSH CODE DATA
            send_data_to_mes(self, self.data_scan1)
            if self.state_ui == False or self.state_ui == None:
                set_state_pass(self)
                self.state_ui = True
            self.THREAD_PLC.send_signal_to_plc(b"1")
            cmd_printer("INFO", f"--> Send Data SN:  {self.data_scan1}")
            logger.info(f"--> Send Data SN:  {self.data_scan1}")

            self.set_default_variables()
            self.is_processing = False

    def set_default_variables(self):
        self.data_scan1 = None

    def display_frame1(self, frame):
        self.frame1 = frame
        frame_zoom_out = cv2.resize(frame, (320, 240))
        frame_rgb = cv2.cvtColor(frame_zoom_out, cv2.COLOR_BGR2RGB)
        img = QImage(
            frame_rgb.data, frame_rgb.shape[1], frame_rgb.shape[0], QImage.Format_RGB888
        )
        scaled_pixmap = img.scaled(self.Uic.CameraFrame1.size())
        pixmap = QPixmap.fromImage(scaled_pixmap)
        self.Uic.CameraFrame1.setPixmap(pixmap)

    def closeEvent(self, event):
        req = QMessageBox.question(
            self,
            "Confirm Close",
            "Do you want to close the application?",
            QMessageBox.Yes | QMessageBox.Cancel,
            QMessageBox.Cancel,
        )
        if req == QMessageBox.Yes:
            event.accept()
            self.THREAD_CAMERA_1.stop()
            self.THREAD_PLC.stop()
            cmd_printer("WARNING", "--------------\nCLOSE")

            # Close Camera and release
            if self.THREAD_CAMERA_1.isRunning():
                # self.THREAD_CAMERA_1.wait()
                self.THREAD_CAMERA_1.cap.release()
            cv2.destroyAllWindows()
        else:
            event.ignore()

    def update_status_camera_error(self):
        self.is_update_cam_error = True
        if self.is_update_cam_error:
            logger.error(f"CAM ERROR")
            self.is_update_cam_error = False
        set_error_camera_state(self)

    def open_camera_thread(self):
        self.THREAD_CAMERA_1 = CameraThread(self.ID_C1)
        self.THREAD_CAMERA_1.frame_received.connect(self.display_frame1)
        self.THREAD_CAMERA_1.start()
        if self.IS_OPEN_CAM_PROPS == 1:
            self.THREAD_CAMERA_1.cap.set(cv2.CAP_PROP_SETTINGS, 1)
        self.THREAD_CAMERA_1.update_error_signal.connect(
            self.update_status_camera_error
        )

        set_default_state(self)
        self.set_default_variables()

    def reconnect_camera_thread(self):
        try:
            if (
                len(self.graph.get_input_devices()) == self.NUM_CAMERA
                and not self.THREAD_CAMERA_1.is_running
            ):
                self.open_camera_thread()
        except Exception as E:
            print(E)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApplication()
    sys.exit(app.exec_())
