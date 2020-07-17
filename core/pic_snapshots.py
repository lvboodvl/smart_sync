# -*- coding: utf-8 -*-
'''
snapshot the screen in two ways:
    1) PIL snow but small file(100KB))
    2) winAPI fast but big file(3MB))
'''
from PIL import ImageGrab
import datetime
import os
import win32gui, win32ui, win32con, win32api

global BASE_DIR
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def PIL_capture(BASE_DIR,filename):
    pic = ImageGrab.grab()
    path=os.path.join(BASE_DIR,'snapshots_imgs',filename)
    pic.save(path)

def window_capture(BASE_DIR,filename):
    hwnd = 0
    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    saveBitMap = win32ui.CreateBitmap()
    MoniterDev = win32api.EnumDisplayMonitors(None, None)
    w = MoniterDev[0][2][2]
    h = MoniterDev[0][2][3]
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    saveDC.SelectObject(saveBitMap)
    saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)
    path=os.path.join(BASE_DIR,'snapshots_imgs',filename)
    saveBitMap.SaveBitmapFile(saveDC, path)

def snapshot_fun():
    now_time = datetime.datetime.now()
    time1 = datetime.datetime.strftime(now_time,'%Y-%m-%d-%H-%M-%S')  
    send_time = str(time1)
    file_name = send_time + ".jpg"
#    window_capture(BASE_DIR,file_name)
    PIL_capture(BASE_DIR,file_name)
    return file_name

if __name__=="__main__":
    file_name = snapshot_fun()
    print(file_name)