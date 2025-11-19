import random
import time

import common.myadb


def nine_nine_nine():
    path = "picture/999/yu_ling_tiao_zhan.png"
    # 使用ADB进行模板匹配和点击
    success = common.myadb.find_and_click_adb(path, "emulator-5554")
    # 准备成功 睡眠3秒 进入成功循环
    print('成功点击挑战,进入循环查询成功界面')
    if success:
        time.sleep(1)
    arr = [
        # "./picture/999/s1.png",
        "./picture/999/yu_ling_success.png",
    ]
    random.shuffle(arr)
    is_success = common.myadb.find_and_click_adb_many_picture(arr)
    if is_success:
        print('成功点击成功，准备迎接挑战')
        time.sleep(random.randint(1, 3))
        return
    time.sleep(1)
    print("\n")


t_start = time.time()
if common.myadb.test_adb_connection() is False:
    print("请先安装ADB并配置环境变量")
else:
    while True:
        # tn = time.time()
        # t_diff = tn - t_start
        # if t_diff / 60 >= 15:
        #     stop_time = random.randint(10, 20)
        #     time.sleep(stop_time * 60)
        #     t_start = time.time()
        #     print(f"执行时间太久 要休息 {t_diff}分钟")
        nine_nine_nine()
