from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer
import sys
from Ui_HALL_260 import Ui_MainWindow
import keyboard
import time
import random

# from pynput.mouse import Controller as MouseCtrl
# from pynput.keyboard import Controller as KeyboardCtrl

# mouse = MouseCtrl()
# keyboard = KeyboardCtrl()
# current_position = mouse.position


class MyApplication(QMainWindow):
    def __init__(self):
        super().__init__()
        self.Uic = Ui_MainWindow()
        self.Uic.setupUi(self)
        self.setWindowTitle("Hall 260    ver:1.0.0.47     Login:V3092552")
        self.show()
        self.Uic.reset_btn.clicked.connect(self.handle_reset)
        keyboard.on_press_key("enter", self.on_enter_event)
        self.txt_results = ["Pass",  "Routing Error"]
        self.count = 0
        self.Uic.txtpackqty.setText(str(self.count))

    def handle_reset(self):
        self.Uic.txtscan.setText(None)
        self.Uic.ruleresult.setText(None)
        self.Uic.txtpackqty.setText(None)
        self.Uic.ruleresult.setStyleSheet(
            "border-color: #fff; background-color: #fff; border-radius: 4px; color: #000"
        )

    def on_enter_event(self, e):
        if e.name == "enter":
            # time.sleep(0.7)
            self.random_result()
            try:
                QTimer.singleShot(0, self.clear_txtscan)
            except Exception as E:
                print(E)

    def clear_txtscan(self):
        self.Uic.txtscan.setText(None)

    def set_result(self):
        self.Uic.ruleresult.setText(self.txt_response)

    def random_result(self):
        probabilities = [1.0, 0.0]
        self.txt_response = random.choices(self.txt_results, weights=probabilities)[0]
        if self.txt_response == "Pass":
            self.count += 1
            self.Uic.txtpackqty.setText(str(self.count))
        try:
            QTimer.singleShot(0, self.set_result)
        except Exception as E:
            print(E)
        print(self.txt_response)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApplication()
    sys.exit(app.exec_())
