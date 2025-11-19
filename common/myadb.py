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


def common_handle_fetch_and_click(template_path, adb: ADBController, screenshot, max_val_set=0.8):
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

    if max_val >= max_val_set:

        x, y = max_loc
        center_x = x + random.randint(1, template.shape[1] - 1)
        center_y = y + random.randint(1, template.shape[0] - 1)

        # 使用ADB点击（不是pyautogui！）
        if adb.tap(center_x, center_y):
            print(f"ADB点击位置: ({center_x}, {center_y})")
            return True

    return False
def common_handle_fetch(template_path, device_id=None, max_val_set=0.8):
    adb = ADBController(device_id)
    # 使用ADB截图（不是pyautogui！）
    screenshot = adb.screenshot()
    if screenshot is None:
        print("ADB截图失败" + device_id)
        return False
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

    print(f"{device_id} 单纯查找 匹配图片{template_path} 匹配度: {max_val:.3f}")

    if max_val >= max_val_set:
         return True

    return False

def rand_click(device_id, center_x, center_y):
    center_x = center_x + random.randint(1, 200 - 1)
    center_y = center_y + random.randint(1, 200 - 1)
    adb = ADBController(device_id)
    if adb.tap(center_x, center_y):
        print(f"{device_id}的ADB点击位置: ({center_x}, {center_y})")
        return True

# 使用示例
def find_and_click_adb(template_path, device_id=None, max_val_set=0.8):
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

        if max_val >= max_val_set:

            x, y = max_loc
            center_x = x + random.randint(1, template.shape[1] - 1)
            center_y = y + random.randint(1, template.shape[0] - 1)

            # 使用ADB点击（不是pyautogui！）
            if adb.tap(center_x, center_y):
                print(f"ADB点击位置: ({center_x}, {center_y})")
                return True

        return False

    except Exception as e:
        print(f"错误: {e}")
        return False


def find_and_click_adb_many_picture(template_path, device_id=None, max_val_set=0.8):
    # 初始化ADB控制器
    adb = ADBController(device_id)
    # 使用ADB截图（不是pyautogui！）
    screenshot = adb.screenshot()
    if screenshot is None:
        print("ADB截图失败")
        return False

    for path in template_path:
        is_find = common_handle_fetch_and_click(path, adb, screenshot, max_val_set)
        if is_find:
            return True
    return False


def find_and_click_adb_many_picture_orb(template_path, device_id=None, min_match_count=10):
    # 初始化ADB控制器
    adb = ADBController(device_id)
    # 使用ADB截图（不是pyautogui！）
    screenshot = adb.screenshot()
    if screenshot is None:
        print("ADB截图失败")
        return False

    for path in template_path:
        is_find = orb_match_and_click(path, screenshot, adb, min_match_count)
        if is_find:
            return True
    return False


def orb_match_and_click(template_path, screenshot, adb, min_match_count=10):
    """
    使用 ORB 特征点进行匹配，并点击目标位置
    """
    # 读取模板
    template = cv2.imread(template_path, cv2.IMREAD_COLOR)
    if template is None:
        print(f"无法读取模板: {template_path}")
        return False

    # 转灰度
    gray_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # 初始化 ORB 检测器
    orb = cv2.ORB_create(nfeatures=1000)

    # 检测并计算特征点
    kp1, des1 = orb.detectAndCompute(gray_template, None)
    kp2, des2 = orb.detectAndCompute(gray_screenshot, None)

    if des1 is None or des2 is None:
        print("未检测到足够特征点")
        return False

    # BF 匹配
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)
    matches = sorted(matches, key=lambda x: x.distance)

    print(f"匹配到 {len(matches)} 个特征点")

    if len(matches) > min_match_count:
        # 取前 N 个点
        src_pts = np.float32([kp1[m.queryIdx].pt for m in matches[:min_match_count]]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in matches[:min_match_count]]).reshape(-1, 1, 2)

        # 计算单应性矩阵
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

        if M is not None:
            h, w = template.shape[:2]
            pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
            dst = cv2.perspectiveTransform(pts, M)

            # 取目标区域中心点
            center_x = int(np.mean(dst[:, 0, 0])) + random.randint(-5, 5)
            center_y = int(np.mean(dst[:, 0, 1])) + random.randint(-5, 5)

            if adb.tap(center_x, center_y):
                print(f"ORB点击位置: ({center_x}, {center_y})")
                return True

    print("ORB匹配失败")
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

def adb_screenshot(device_id, region=None):
    """
    截图并裁剪
    :param device_id: adb 设备号
    :param region: (x, y, w, h) 指定区域，None 表示全屏
    """
    result = subprocess.run(
        ["adb", "-s", device_id, "exec-out", "screencap", "-p"],
        stdout=subprocess.PIPE
    )
    img = cv2.imdecode(np.frombuffer(result.stdout, np.uint8), cv2.IMREAD_COLOR)
    if region:
        x, y, w, h = region
        img = img[y:y+h, x:x+w]
    return img

# 示例：截取 emulator-5554 的 (100, 200, 300, 400) 区域
