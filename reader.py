from libs.libs import cv2, decode, zxingcpp


def read_dmt_zxingcpp(frame):
    data_decoded = zxingcpp.read_barcodes(frame)
    if data_decoded:
        return data_decoded[0].text
    return read_dmt_pylibdmtx(frame)


def read_dmt_pylibdmtx(frame):
    data = decode(frame, timeout=50, max_count=1)
    if data != []:
        data = data[0][0].decode("utf-8")
        print("data: ", data)
        return data
    return None


def read_dmt_loop(self, frame):
    for threshold in range(self.MIN_THRESH, self.MAX_THRESH, self.THRESH_JUMP):
        _, thresh = cv2.threshold(frame, threshold, self.MAX_THRESH, cv2.THRESH_BINARY)
        data_decoded = zxingcpp.read_barcodes(thresh)
        if data_decoded:
            return data_decoded[0].text
        else:
            data = decode(frame, timeout=50, max_count=1)
            if data != []:
                data = data[0][0].decode("utf-8")
                print("data: ", data)
                return data
    return None


def process_frame(frame):
    frame = cv2.resize(frame, None, fx=1.2, fy=1.2)
    blur = cv2.GaussianBlur(frame, (5, 5), 0)
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    return gray
