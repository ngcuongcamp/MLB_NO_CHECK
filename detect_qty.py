import pytesseract
import cv2
import numpy as np
from PIL import ImageGrab
import pytesseract
import pyautogui


def capture_screen():
    screenshot = np.array(ImageGrab.grab())
    # w, h, _ = screenshot.shape
    # print(f"Size of screen image: {w} x {h}")
    screenshot = screenshot[334:364, 926:1012]
    # screenshot = screenshot[822:1024, 362:382]

    # (L926, T334, R1012, B364)
    # height, width = screenshot.shape[:2]
    # screenshot = cv2.resize(screenshot, (width * 2, height * 2))
    # cv2.imshow("screenshot", screenshot)
    # cv2.waitKey(0)
    return screenshot


def detect_label(screenshot):
    pytesseract.pytesseract.tesseract_cmd = (
        # r"libs\tesseract\Tesseract-OCR\tesseract.exe"
        # D:\SD_CODE\libs\tesseract\Tesseract-OCR
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )
    # config = "--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ</"
    # config = r"--oem 3 --psm 6"
    config = "--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789</"
    try:
        str_label = pytesseract.image_to_string(screenshot, config=config)
        print('test', str_label)
        txt_result = str_label.strip().split(" ")[-1]
        # # txt_result = "".join([char for char in txt_result if char.isdigit()])
        return txt_result
    except Exception as E:
        print(E)
    # return 1


# scr = capture_screen()
# txt = detect_label(scr)
