import common.myadb
import cv2
import time
import random
from concurrent.futures import ThreadPoolExecutor

my = 'emulator-5554'
host = 'emulator-5574'


def click_tiao_zhan():
    success = common.myadb.find_and_click_adb_many_picture(['./picture/yuhun/tiaozhan.png'], host)
    # success = common.myadb.find_and_click_adb_many_picture(['./picture/yuhun/bb.jpg'], "127.0.0.1:16416")
    print(f'查看自有匹配结果 {success}')


def click_chenggong():
    # success = common.myadb.find_and_click_adb_many_picture(['./picture/yuhun/finish1.png'], host)
    # success = common.myadb.find_and_click_adb_many_picture(['./picture/yuhun/finish1.png'], my)
    # success = common.myadb.find_and_click_adb_many_picture(['./picture/yuhun/finish2.png'], host)
    # success = common.myadb.find_and_click_adb_many_picture(['./picture/yuhun/finish2.png'], my)
    # 前两行并发执行
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(common.myadb.find_and_click_adb_many_picture,
                        ['./picture/yuhun/finish1.png'], host)
        executor.submit(common.myadb.find_and_click_adb_many_picture,
                        ['./picture/yuhun/yu_hun_tmp_jie_mian.png'], host, 0.6)
        executor.submit(common.myadb.find_and_click_adb_many_picture,
                        ['./picture/yuhun/finish2.png'], host)

    # 后两行并发执行
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(common.myadb.find_and_click_adb_many_picture,
                        ['./picture/yuhun/finish1.png'], my)
        executor.submit(common.myadb.find_and_click_adb_many_picture,
                        ['./picture/yuhun/yu_hun_tmp_jie_mian.png'], my, 0.6)
        executor.submit(common.myadb.find_and_click_adb_many_picture,
                        ['./picture/yuhun/finish2.png'], my)


tn = time.time()
while True:
    click_tiao_zhan()
    click_chenggong()
    time.sleep(random.uniform(0, 1))  # 随机生成 [1,5] 的浮点数
    # tnw = time.time()
    # if tnw - tn > 30 * 60:
    #     print("运行超过20分钟了，该睡眠一会儿")
    #     time.sleep(60 * random.uniform(3, 7))

# screenshot = common.myadb.adb_screenshot("emulator-5554", (0, 0, 700, 700))
# cv2.imwrite("tiao_zhan2.png", screenshot)
# screenshot = common.myadb.adb_screenshot("127.0.0.1:16416", (1750, 900, 150, 130))
# cv2.imwrite("picture/yuhun/tiaozhan.png", screenshot)
