import os
import time
import keyboard
from PIL import ImageGrab

os.chdir("C:/Users/hooni/Documents/coding/nadocoding/3_gui_basic/gui_project/images")

def screenshot():
    # 2020년 6월 1일 10시 20분 30 초 -> _20200601_102030
    curr_time = time.strftime("_%Y%m%d_%H%M%S")
    img = ImageGrab.grab()
    img.save("image{}.png".format(curr_time)) # ex) image_20200601_102030.png


keyboard.add_hotkey("F9", screenshot) # 사용자가 F9 키를 누르면 스크린 샷 저장

keyboard.wait("esc") # 사용자가 esc 를 누를 때까지 프로그램 수행