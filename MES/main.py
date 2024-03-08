from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer, Qt
import sys
from Ui_MES import Ui_MainWindow
import keyboard
import time
import random
from colorama import Fore, Back, Style, init, AnsiToWin32


init(wrap=False)
stream = AnsiToWin32(sys.stderr).stream


class MyApplication(QMainWindow):
    def __init__(self):
        super().__init__()
        self.Uic = Ui_MainWindow()
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.Uic.setupUi(self)
        self.setWindowTitle("H0-51    ver:1.0.0.47     Login:V3092552")
        self.show()
        self.Uic.reset_btn.clicked.connect(self.handle_reset)
        keyboard.on_press_key("enter", self.on_enter_event)
        self.msg_list_1 = [
            "Please scan lot no",
            "Repetitive operation",
            "Routing Erorr",
        ]
        self.msg_list_2 = ["Save Error", "Pass"]
        self.operation_arr = [False, False]
        self.count = 0
        self.Uic.lblMoveOUTQTY.setText(str(self.count))

    def handle_reset(self):
        self.Uic.txtscan.setText(None)
        self.Uic.ruleresult.setText(None)
        self.Uic.lblMoveOUTQTY.setText(None)

    def on_enter_event(self, e):
        if e.name == "enter":
            time.sleep(0.1)
            if self.operation_arr == [False, False]:
                self.random_msg_1()
                # print("SN RESPONSE: ", self.txt_response)
                print(Fore.YELLOW + "SN RESPONSE: " + self.txt_response, file=stream)
            elif self.operation_arr == [True, False]:
                self.random_msg_2()
                # print("FIXTURE RESPONSE: ", self.txt_response)
                print(
                    Fore.GREEN + "FIXTURE RESPONSE: " + self.txt_response, file=stream
                )

            try:
                QTimer.singleShot(0, self.clear_txtscan)
            except Exception as E:
                print(E)

    def clear_txtscan(self):
        self.Uic.txtscan.setText(None)

    def random_msg_1(self):
        probabilities = [0.6, 0.3, 0.1]
        self.txt_response = random.choices(self.msg_list_1, weights=probabilities)[0]
        try:
            QTimer.singleShot(0, self.set_result_msg)
            if (
                self.txt_response == "Repetitive operation"
                or self.txt_response == "Routing Erorr"
            ):
                self.operation_arr = [False, False]
            else:
                self.operation_arr[0] = True

        except Exception as E:
            print(E)

    def random_msg_2(self):
        probabilities = [0.2, 0.8]
        self.txt_response = random.choices(self.msg_list_2, weights=probabilities)[0]
        try:
            QTimer.singleShot(0, self.set_result_msg)
            if self.txt_response == "Pass":
                self.count += 1
                self.Uic.lblMoveOUTQTY.setText(str(self.count))
            self.operation_arr = [False, False]
        except Exception as E:
            print(E)

    def set_result_msg(self):
        self.Uic.ruleresult.setText(self.txt_response)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApplication()
    sys.exit(app.exec_())
