from libs.libs import (
    Desktop,
    pywinauto,
    Application,
    time,
    pyautogui,
    send_keys,
    keyboard,
)
from utilities import logger, cmd_printer
from UI_handler import set_error_mes_state


def get_name_mes_app(self):
    print(self.MES_APP_NAME)
    top_windows = Desktop(backend=self.MES_BACKEND).windows()
    is_found = False
    for w in top_windows:
        if "login:" in w.window_text().lower() and "ver:" in w.window_text().lower():
            self.MES_APP_NAME = w.window_text()
            is_found = True
            break
    if is_found == False:
        set_error_mes_state(self)
        print("Can't connect with MES APP")
        logger.error("Can't connect with MES APP")


def get_title_obj(self, auto_id):
    # print(self.MES_APP_NAME)
    try:
        export = pywinauto.findwindows.find_windows(best_match=self.MES_APP_NAME)
        if export:
            app = Application(backend=self.MES_BACKEND).connect(handle=export[0])
            dialog = app.window(title=self.MES_APP_NAME)
            obj = dialog.child_window(auto_id=auto_id)
            # txt_obj = obj.wrapper_object().window_text()
            txt_obj = obj.window_text()
            return txt_obj
    except Exception as E:
        set_error_mes_state(self)


# def send_data_to_mes(self, data: str):
#     print(self.MES_APP_NAME)
#     try:
#         export = pywinauto.findwindows.find_windows(best_match=self.MES_APP_NAME)
#         if export:
#             app = Application(backend=self.MES_BACKEND).connect(handle=export[0])
#             dialog = app.window(title=self.MES_APP_NAME)
#             input = dialog.child_window(auto_id=self.MES_INPUT_AUTO_ID)
#             input.type_keys(data)
#             input.type_keys("{ENTER}")

#     except Exception as E:
#         set_error_mes_state(self)
#         logger.error("Failed to push code because the app is not connected.")


def send_data_to_mes(self, data: str):
    cmd_printer("INFO", "Start send")
    x = 1024 / 2
    y = 768 / 2
    pyautogui.moveTo(x, y)
    pyautogui.typewrite(data)
    pyautogui.moveTo(x, y)
    keyboard.press_and_release("enter")
    cmd_printer("INFO", "End send")
    print(self.THREAD_PLC)


