import common.myadb
import cv2

screenshot = common.myadb.adb_screenshot("emulator-5554", (1245, 740, 260, 70))
cv2.imwrite("picture/jvjue.png", screenshot)
# screenshot = common.myadb.adb_screenshot("127.0.0.1:16416", (1750, 900, 150, 130))
# cv2.imwrite("picture/yuhun/tiaozhan.png", screenshot)