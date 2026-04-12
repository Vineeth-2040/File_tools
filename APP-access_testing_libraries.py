import subprocess
import time
import pyautogui

subprocess.Popen(["code", "--new-window", r"E:\HRTF"])
time.sleep(10)
pyautogui.hotkey("alt", "F4")  # maximize window