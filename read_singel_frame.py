import cv2
import zxingcpp
from pylibdmtx.pylibdmtx import decode

image = cv2.imread("./images/image_6.png")
image = cv2.resize(image, None, fx=1.2, fy=1.2)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5, 5), 0)
# blur = cv2.GaussianBlur(gray, ksize=(3, 3), sigmaX=3, sigmaY=3)

cv2.imshow("blur", blur)

decoded = zxingcpp.read_barcodes(blur)
if decoded != []:
    print(decoded[0].text)
else:
    decoded = decode(blur, timeout=50)
    if decoded != []:
        decoded = decoded[0][0].decode("utf-8")
        print(decoded)
    else:
        print(None)

cv2.imshow("gray", gray)
cv2.waitKey(0)
