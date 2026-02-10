import common.myadb
import time

my = 'emulator-5554'


def jiejieFunc():
    is_fetch_jingong = common.myadb.common_handle_fetch("./picture/jiejie/jin_gong.png", my)
    is_fetch_yin_yang_liao = common.myadb.common_handle_fetch("./picture/jiejie/yin_yang_liao_logo.png", my)
    # 说明在界面上

    if is_fetch_yin_yang_liao:
        print("找到了阴阳寮的logo")
        if is_fetch_jingong:
            print("找到了进攻的logo")
            common.myadb.find_and_click_adb_many_picture(["./picture/jiejie/jin_gong.png"], my)
        else:
            print("随机点击")
            common.myadb.rand_click_by_four_point(my, 1300, 840, 1500, 900)
    is_success = common.myadb.find_and_click_adb_many_picture(["./picture/jiejie/success.png"], my)
    if is_success:
        return
    common.myadb.find_and_click_adb_many_picture(["./picture/jiejie/fail.png"], my)

while True:
    jiejieFunc()
    time.sleep(1)
