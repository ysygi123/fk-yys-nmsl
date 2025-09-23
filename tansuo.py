import time

import common.myadb

need_tan_suo = False

def tan_suo():
    # tan_suo_click = ['./picture/tansuo/tansuo.png']
    # success = common.myadb.find_and_click_adb_many_picture_orb(tan_suo_click, None)
    # if success is False:
    #     print("点击探索失败")
    #     return
    # time.sleep(2)
    success = common.myadb.find_and_click_adb_many_picture_orb(['./picture/tansuo/k28.png'])
    print(f'查看点击困28结果 {success}')
    return


tan_suo()