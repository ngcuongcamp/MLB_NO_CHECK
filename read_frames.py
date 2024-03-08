import cv2
from pylibdmtx.pylibdmtx import decode
import zxingcpp
import os
import time

path = "./images"


def process_frame(frame):
    frame = cv2.resize(frame, None, fx=1.2, fy=1.2)
    filt = cv2.GaussianBlur(src=frame, ksize=(5, 5), sigmaX=3, sigmaY=3)
    gray = cv2.cvtColor(filt, cv2.COLOR_BGR2GRAY)
    return gray


def read_dmt_pylibdmtx(img):
    img = cv2.resize(img, None, fx=1.2, fy=1.2)
    filt = cv2.GaussianBlur(src=img, ksize=(5, 5), sigmaX=3, sigmaY=3)
    gray = cv2.cvtColor(filt, cv2.COLOR_BGR2GRAY)

    for threshold in range(30, 170, 3):
        _, thresh = cv2.threshold(gray, threshold, 200, cv2.THRESH_BINARY)
        cv2.imshow("thresh", thresh)
        cv2.waitKey(1)

        data = decode(thresh, timeout=50)
        if data != []:
            data = data[0][0].decode("utf-8")
            print("data: ", data)
            return data


def read_dmt_zxingcpp(gray):
    for threshold in range(30, 170, 3):
        _, thresh = cv2.threshold(gray, threshold, 200, cv2.THRESH_BINARY)
        data_decoded = zxingcpp.read_barcodes(thresh)
        if data_decoded:
            print("thresh: ", threshold)
            return data_decoded[0].text


for index in os.scandir(path=path):
    frame = cv2.imread(index.path)
    gray = process_frame(frame)

    #  read gray by zxingcpp
    data = zxingcpp.read_barcodes(gray)
    if data:
        data = data[0].text
        print("Zxingcpp gray: ", data)
    else:
        #   read gray by pylibdmtx
        # data = decode(gray, timeout=50)
        # if data != []:
        #     data = data[0][0].decode("utf-8")
        #     print("Pylibdmtx gray: ", data)
        # else:
        #     data = read_dmt_zxingcpp(gray)
        #     if data is None:
        print("xxxxxxxxxxxxxxxxxxxxxxx")


# a = 0
# start_time_pylibdmtx = time.time()
# for i in os.scandir(path):
#     a += 1
#     frame = cv2.imread(i.path)
#     img = frame
#     data = read_Qr_pylibdmtx(img)
#     print(f"pylibdmtx - data {a}: {data}")
#     cv2.waitKey(1)
# end_time_pylibdmtx = time.time()
# print(f"Time taken by pylibdmtx: {end_time_pylibdmtx - start_time_pylibdmtx} seconds")

# a = 0
# start_time_zxingcpp = time.time()
# for i in os.scandir(path):
#     a += 1
#     frame = cv2.imread(i.path)
#     img = frame
#     data = read_dmt_zxingcpp(img)
#     print(f"zxingcpp - data {a}: {data}")
#     cv2.waitKey(1)
# end_time_zxingcpp = time.time()
# print(f"Time taken by zxingcpp: {end_time_zxingcpp - start_time_zxingcpp} seconds")

cv2.destroyAllWindows()
