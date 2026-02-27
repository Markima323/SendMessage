"""
Windows auto clicker & typer (clipboard-based, supports中文).
Usage:
1) 安装依赖: pip install --upgrade pyautogui keyboard pillow pyperclip
2) 运行脚本: python 1.py
3) 把鼠标移动到目标输入框，按 F8 记录坐标，3 秒后自动开始循环点击+粘贴+回车。
按 ESC 可随时中止；把鼠标甩到屏幕角也会触发 pyautogui failsafe。
"""

import sys
import time
import random
import os
import sysconfig
import site


def ensure_site_packages():
    """确保嵌入式/便携版 Python 也能找到已安装的第三方库。"""
    candidates = set()
    for key in ("purelib", "platlib"):
        try:
            candidates.add(sysconfig.get_paths().get(key))
        except Exception:
            pass
    try:
        candidates.add(site.getusersitepackages())
    except Exception:
        pass
    for path in candidates:
        if path and os.path.isdir(path) and path not in sys.path:
            sys.path.append(path)


ensure_site_packages()

try:
    import pyautogui
    import keyboard
    import pyperclip
except ImportError as e:
    missing = getattr(e, "name", str(e))
    py_path = sys.executable
    py_ver = sys.version.split()[0]
    print(
        f"缺少依赖: {missing}\n"
        f"当前 Python: {py_path}\n"
        f"版本: {py_ver}\n"
        f"请用当前解释器安装: \"{py_path}\" -m pip install --upgrade pyautogui keyboard pillow pyperclip"
    )
    sys.exit(1)

# ----- 可修改参数 -----
MESSAGES = [
  "钱什么时候还？请给具体时间。",
]
REPEAT = 999999999999999                           # 发送次数
DELAY_BETWEEN = 6                   # 每次发送后的停顿（秒）
CAPTURE_HOTKEY = "f8"                 # 记录光标位置的按键
STOP_KEY = "esc"                      # 中途停止的按键
RUN_WINDOW = 10 * 60                   # 连续运行多久后休息（秒）
REST_WINDOW = 1 * 60                  # 休息时长（秒）
# ----------------------

pyautogui.FAILSAFE = True  # 鼠标移到屏幕角可强制中止


def capture_position():
    print(f"请把鼠标移动到目标输入框，然后按 {CAPTURE_HOTKEY.upper()} 记录坐标...")
    keyboard.wait(CAPTURE_HOTKEY)
    pos = pyautogui.position()
    print(f"已记录 {pos}，3 秒后开始，请切换到目标窗口。")
    for i in range(3, 0, -1):
        print(f"{i}...", end="", flush=True)
        time.sleep(1)
    print()
    return pos


def send_once(target, text):
    pyautogui.click(target)       # 确保焦点在输入框
    time.sleep(0.1)
    pyperclip.copy(text)          # 用剪贴板，避免中文/IME 不能直接键入的问题
    pyautogui.hotkey("ctrl", "v")
    pyautogui.press("enter")


def rest_if_needed(start_ts):
    """每运行 RUN_WINDOW 秒就休息 REST_WINDOW 秒，返回新的起始时间。"""
    elapsed = time.monotonic() - start_ts
    if elapsed < RUN_WINDOW:
        return start_ts

    print(f"已连续运行约 {RUN_WINDOW // 60} 分钟，休息 {REST_WINDOW // 60} 分钟...")
    for _ in range(REST_WINDOW):
        if keyboard.is_pressed(STOP_KEY):
            print("休息中检测到停止键，已中止。")
            sys.exit(0)
        time.sleep(1)
    print("休息结束，继续。")
    return time.monotonic()


def main():
    target = capture_position()
    window_start = time.monotonic()

    for n in range(1, REPEAT + 1):
        if keyboard.is_pressed(STOP_KEY):
            print("检测到停止键，已中止。")
            return
        text = random.choice(MESSAGES)
        send_once(target, text)
        print(f"已发送 {n}/{REPEAT}（本次内容：{text}）")
        time.sleep(DELAY_BETWEEN)
        window_start = rest_if_needed(window_start)

    print("完成。")


if __name__ == "__main__":
    main()
