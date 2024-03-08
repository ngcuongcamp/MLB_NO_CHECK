import keyboard
import pyautogui
import time
import cv2
from utilities import cmd_printer
import pyscreeze
import numpy as np
import pytesseract

from detect_qty import capture_screen, detect_label

def send_data_to_mes(data: str):
    cmd_printer("INFO", "Start send")
    x = 1024 / 2
    y = 768 / 2
    time.sleep(3)
    pyautogui.moveTo(x, y)
    pyautogui.typewrite(data)
    pyautogui.moveTo(x, y)
    keyboard.press_and_release("enter")
    scr = capture_screen()
    cv2.imshow("screenshot", scr)
    cv2.waitKey(0)
    txt = detect_label(scr)
    print("test", txt)
    cmd_printer("INFO", "End send")

# (L882, T362, R1025, B383)
# send_data_to_mes("test")
def capture_screen():
    time.sleep(2)
    # screenshot = pyscreeze.screenshot(region=(882, 362, 142, 21 ))
    screenshot = pyscreeze.screenshot(region=(882, 362, 142, 18))


    screenshot = np.array(screenshot)

    # height, width = screenshot.shape[:2]
    # screenshot = cv2.resize(screenshot, (width * 2, height * 2))

    # cv2.imshow('screenshot', screenshot)
    # cv2.waitKey(0)
    return screenshot
# screenshot = capture_screen()



def detect_qty():
    pytesseract.pytesseract.tesseract_cmd = (
        # r"libs\tesseract\Tesseract-OCR\tesseract.exe"
        # D:\SD_CODE\libs\tesseract\Tesseract-OCR
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )
    # config = "--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ</"
    # config = r"--oem 3 --psm 6"
    config = "--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789</"
    try:
        screenshot = capture_screen()
        str_label = pytesseract.image_to_string(screenshot, config=config)
        # str_label = pytesseract.image_to_string(screenshot)
        # txt_result = str_label.strip().split(" ")[-1]
        # # txt_result = "".join([char for char in txt_result if char.isdigit()])
        return str_label
    except Exception as E:
        print(E)

img1 = capture_screen()
cv2.imshow('img1', img1)
cv2.waitKey(0)
time.sleep(2)

img2 = capture_screen()
cv2.imshow('img2', img2)
cv2.waitKey(0)


img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

percent_match = cv2.matchTemplate(img1, img2, cv2.TM_CCOEFF_NORMED)[0][0]
print('percent_match', percent_match)

cv2.imshow('1', img1)
cv2.imshow('2', img2)
cv2.waitKey(0)


