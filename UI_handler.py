from libs.libs import QDesktopWidget, QPixmap, Qt, QIcon, Ui_MainWindow


#! UI functions handler


def initial_UI_MainWindow(self):
    self.Uic = Ui_MainWindow()
    self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
    self.Uic.setupUi(self)
    self.setWindowTitle("MLB 473")
    self.setWindowIcon(QIcon("./icons/Logo.ico"))
    # set position window
    screen_geometry = QDesktopWidget().availableGeometry()
    self.setGeometry(
        screen_geometry.width() - self.width(),
        screen_geometry.height() - self.height(),
        self.width(),
        self.height(),
    )

    # origin background
    original_pixmap = QPixmap("./icons/bg_1camera.png")
    scaled_pixmap = original_pixmap.scaled(
        self.Uic.CameraFrame1.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
    )
    self.Uic.CameraFrame1.setPixmap(scaled_pixmap)

    # handle click update button
    self.Uic.UpdateButton.clicked.connect(self.handle_click_update)
    self.show()


def set_state(
    self,
    background_color,
    text_color,
    button_background_color,
    button_text_color,
    result_text,
):
    self.Uic.ResultContent.setStyleSheet(
        f'background-color: {background_color}; font: 14pt "Segoe UI";border: 1px solid #ccc; color: {text_color}'
    )
    self.Uic.ResultContent.setText(result_text)
    self.Uic.UpdateButton.setStyleSheet(
        f"background-color: {button_background_color}; color: {button_text_color}; border: 1px solid #fff; border-radius: 8px;"
    )


def set_state_pass(self):
    set_state(self, "#32a852", "#fff", "#fff", "#006f00", "PASS")


def set_fail_state(self):
    set_state(self, "#b84935", "#fff", "#fff", "#b84935", "FAIL")


def set_default_state(self):
    set_state(self, "#fff", "#999", "#006f00", "#fff", "NONE")


def set_reset_state(self):
    set_state(self, "#fff", "#006f00", "#006f00", "#fff", "RESET")


def set_error_camera_state(self):
    set_state(self, "#a84632", "#fff", "#b84935", "#fff", "CAM ERROR")
    original_pixmap = QPixmap("./icons/bg_1camera.png")
    scaled_pixmap = original_pixmap.scaled(
        self.Uic.CameraFrame1.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
    )
    self.Uic.CameraFrame1.setPixmap(scaled_pixmap)


def set_error_mes_state(self):
    set_state(self, "#b84935", "#fff", "#fff", "#b84935", "OPEN MES?")
