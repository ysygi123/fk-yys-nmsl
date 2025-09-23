import random
from ctypes import pythonapi

import cv2
import numpy as np
import subprocess
import os

class ADBController:
    def __init__(self, device_id=None):
        self.device_id = device_id

    def run_adb(self, cmd):
        """执行ADB命令"""
        if self.device_id:
            full_cmd = f"adb -s {self.device_id} {cmd}"
        else:
            full_cmd = f"adb {cmd}"

        try:
            result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True)
            return result.returncode == 0, result.stdout
        except Exception as e:
            return False, str(e)

    def screenshot(self):
        """使用ADB截图（不需要pyautogui！）"""
        try:
            # 方法1：直接获取二进制数据（推荐）
            if self.device_id:
                cmd = ['adb', '-s', self.device_id, 'exec-out', 'screencap', '-p']
            else:
                cmd = ['adb', 'exec-out', 'screencap', '-p']

            result = subprocess.run(cmd, capture_output=True)
            if result.returncode == 0:
                # 将二进制数据转换为numpy数组
                image_array = np.frombuffer(result.stdout, dtype=np.uint8)
                screenshot = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
                return screenshot

            # 方法2：传统方式（如果方法1失败）
            temp_file = "/sdcard/screenshot.png"
            local_file = "temp_screenshot.png"

            # 截图并拉取
            self.run_adb(f"shell screencap -p {temp_file}")
            self.run_adb(f"pull {temp_file} {local_file}")
            self.run_adb(f"shell rm {temp_file}")

            # 读取图像
            screenshot = cv2.imread(local_file)
            os.remove(local_file)  # 清理临时文件

            return screenshot

        except Exception as e:
            print(f"截图失败: {e}")
            return None

    def tap(self, x, y):
        """使用ADB点击（不需要pyautogui！）"""
        return self.run_adb(f"shell input tap {x} {y}")[0]

    def swipe(self, x1, y1, x2, y2, duration=300):
        """使用ADB滑动"""
        return self.run_adb(f"shell input swipe {x1} {y1} {x2} {y2} {duration}")[0]

    def keyevent(self, keycode):
        """发送按键事件"""
        return self.run_adb(f"shell input keyevent {keycode}")[0]

def common_handle_fetch_and_click(template_path, adb: ADBController, screenshot):
    # 读取模板
    template = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
    if template is None:
        print(f"无法读取模板: {template_path}")
        return False
    if len(template.shape) == 3 and template.shape[2] == 4:
        template_img = template[:, :, :3]
        mask = template[:, :, 3]
        result = cv2.matchTemplate(screenshot, template_img, cv2.TM_CCOEFF_NORMED, mask=mask)
    else:
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    print(f"匹配图片{template_path} 匹配度: {max_val:.3f}")

    if max_val >= 0.8:

        x, y = max_loc
        center_x = x + random.randint(1, template.shape[1] - 1)
        center_y = y + random.randint(1, template.shape[0] - 1)

        # 使用ADB点击（不是pyautogui！）
        if adb.tap(center_x, center_y):
            print(f"ADB点击位置: ({center_x}, {center_y})")
            return True

    return False

# 使用示例
def find_and_click_adb(template_path, device_id=None):
    """
    使用ADB进行模板匹配和点击
    """
    try:
        # 初始化ADB控制器
        adb = ADBController(device_id)

        # 读取模板
        template = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)
        if template is None:
            print(f"无法读取模板: {template_path}")
            return False

        # 使用ADB截图（不是pyautogui！）
        screenshot = adb.screenshot()
        if screenshot is None:
            print("ADB截图失败")
            return False

        # 处理带透明度的模板
        if len(template.shape) == 3 and template.shape[2] == 4:
            template_img = template[:, :, :3]
            mask = template[:, :, 3]
            result = cv2.matchTemplate(screenshot, template_img, cv2.TM_CCOEFF_NORMED, mask=mask)
        else:
            result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        print(f"匹配图片{template_path} 匹配度: {max_val:.3f}")

        if max_val >= 0.8:

            x, y = max_loc
            center_x = x +  random.randint(1, template.shape[1] - 1)
            center_y = y + random.randint(1, template.shape[0]-1)

            # 使用ADB点击（不是pyautogui！）
            if adb.tap(center_x, center_y):
                print(f"ADB点击位置: ({center_x}, {center_y})")
                return True

        return False

    except Exception as e:
        print(f"错误: {e}")
        return False

def find_and_click_adb_many_picture(template_path, device_id=None):
    # 初始化ADB控制器
    adb = ADBController(device_id)
    # 使用ADB截图（不是pyautogui！）
    screenshot = adb.screenshot()
    if screenshot is None:
        print("ADB截图失败")
        return False

    for path in template_path:
        is_find = common_handle_fetch_and_click(path, adb, screenshot)
        if is_find:
            return True
    return False
# 连接测试
def test_adb_connection():
    """测试ADB连接"""
    try:
        result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
        print("ADB设备列表:")
        print(result.stdout)
        return True
    except:
        print("ADB未安装或未在PATH中")
        return False


