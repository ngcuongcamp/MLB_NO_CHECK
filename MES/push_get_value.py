from pywinauto.application import Application
import pywinauto
from pywinauto import Desktop
import configparser
import time

config = configparser.ConfigParser()
config.read("./test.ini")
import keyboard
import pyautogui

BACKEND = config["TEST"]["BACKEND"]
OPTION_RUN = int(config["TEST"]["OPTION_RUN"])
APP_NAME = config["TEST"]["APP_NAME"]
INPUT_AUTO_ID = config["TEST"]["INPUT_AUTO_ID"]
INPUT_CLASS_NAME = config["TEST"]["INPUT_CLASS_NAME"]
RESULT_AUTO_ID = config["TEST"]["RESULT_AUTO_ID"]
RESULT_CLASS_NAME = config["TEST"]["RESULT_CLASS_NAME"]
TIME_SLEEP = float(config["TEST"]["TIME_SLEEP"])
IS_USE_CLASS_NAME = int(config["TEST"]["IS_USE_CLASS_NAME"])
IS_FIND_MOVE_OUT_ELEMENT = int(config["TEST"]["IS_FIND_MOVE_OUT_ELEMENT"])
MOVE_OUT_AUTO_ID = config["TEST"]["MOVE_OUT_AUTO_ID"]
MOVE_OUT_CLASS_NAME = config["TEST"]["MOVE_OUT_CLASS_NAME"]
OPTION_ENTER_PRESS = config["TEST"]["OPTION_ENTER_PRESS"]


def write_log_test(file_path, content, mode="a"):
    try:
        with open(file_path, mode) as file:
            file.write(content)
    except Exception as e:
        print("e")


if OPTION_RUN == 1:
    top_windows = Desktop(backend=BACKEND).windows()
    for w in top_windows:
        print(w.window_text())

elif OPTION_RUN == 2:
    try:
        export = pywinauto.findwindows.find_windows(best_match=APP_NAME)
        if export:
            app = Application(backend="uia").connect(handle=export[0])
            dialog = app.window(title=APP_NAME)
            dialog.print_control_identifiers()
    except Exception as e:
        print("error:", e)

elif OPTION_RUN == 3:
    data = "CODETESTHERE"
    while True:
        print("\n----START PUSH----\n")
        write_log_test("./note.txt", "\n----START PUSH----\n")
        try:
            export = pywinauto.findwindows.find_windows(best_match=APP_NAME)
            if export:
                app = Application(backend=BACKEND).connect(handle=export[0])
                dialog = app.window(title=APP_NAME)

                input = None
                if IS_USE_CLASS_NAME == 1:
                    input = dialog.child_window(class_name=INPUT_CLASS_NAME)
                else:
                    input = dialog.child_window(auto_id=INPUT_AUTO_ID)
                input.type_keys(data)

                if OPTION_ENTER_PRESS == "0":
                    input.type_keys("{ENTER}")
                elif OPTION_ENTER_PRESS == "1":
                    dialog.type_keys("{ENTER}")
                elif OPTION_ENTER_PRESS == "2":
                    keyboard.press_and_release("enter")
                elif OPTION_ENTER_PRESS == "3":
                    pyautogui.press("enter")

                print("....Sleep 1s....\n")
                write_log_test("./note.txt", "....Sleep 1s....\n")
                time.sleep(TIME_SLEEP)

                print("------ get infomation ------\n")
                # GET INFOMATIONE
                info_msg = None

                if IS_USE_CLASS_NAME == 1:
                    info_msg = dialog.child_window(class_name=RESULT_CLASS_NAME)
                else:
                    info_msg = dialog.child_window(auto_id=RESULT_AUTO_ID)

                txt_info_msg = info_msg.wrapper_object().window_text()
                write_log_test("./note.txt", "---INFOMATION---\n")
                write_log_test("./note.txt", txt_info_msg)
                write_log_test("./note.txt", "\n--------------------------\n")

                print("---INFOMATION---")
                print(txt_info_msg)

                # GET MOVE OUT TEXT
                if IS_FIND_MOVE_OUT_ELEMENT == 1:
                    moveout_element = None
                    if IS_USE_CLASS_NAME == 1:
                        moveout_element = dialog.child_window(
                            class_name=MOVE_OUT_CLASS_NAME
                        )
                    else:
                        moveout_element = dialog.child_window(auto_id=MOVE_OUT_AUTO_ID)
                    txt_moveout = moveout_element.wrapper_object().window_text()
                    print("\n--------MOVEOUT---------\n")
                    print(txt_moveout)

                    write_log_test("./note.txt", "\n--------MOVEOUT---\n")
                    write_log_test("./note.txt", txt_moveout)
                    write_log_test("./note.txt", "\n--------------------------\n")

                print("\n--------------------------\n")
        except Exception as E:
            print(E)
