import common.myadb
import cv2

def click_tiao_zhan():
    success = common.myadb.find_and_click_adb_many_picture(['./picture/yuhun/tiaozhan.png'], "127.0.0.1:16416")
    # success = common.myadb.find_and_click_adb_many_picture(['./picture/yuhun/bb.jpg'], "127.0.0.1:16416")
    print(f'查看自有匹配结果 {success}')

def click_chenggong():
    success = common.myadb.find_and_click_adb_many_picture(['./picture/yuhun/finish1.png'], "127.0.0.1:16416")
    success = common.myadb.find_and_click_adb_many_picture(['./picture/yuhun/finish1.png'], "emulator-5554")
    success = common.myadb.find_and_click_adb_many_picture(['./picture/yuhun/finish2.png'], "127.0.0.1:16416")
    success = common.myadb.find_and_click_adb_many_picture(['./picture/yuhun/finish2.png'], "emulator-5554")


while True:
    click_tiao_zhan()
    click_chenggong()


# screenshot = common.myadb.adb_screenshot("emulator-5554", (0, 0, 700, 700))
# cv2.imwrite("partial.png", screenshot)
# screenshot = common.myadb.adb_screenshot("127.0.0.1:16416", (1750, 900, 150, 130))
# cv2.imwrite("picture/yuhun/tiaozhan.png", screenshot)
