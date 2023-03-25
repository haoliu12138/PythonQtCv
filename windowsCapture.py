import ctypes.wintypes
import numpy as np
import win32gui,win32ui,win32con
from threading import Thread,Lock
import cv2 as cv
import time
class WindowCapture:
    # 截取宽高
    w=0
    h=0
    hwnd=None
    # 截图
    img=None
    # 停止标志
    stopped=True
    # 构造函数
    def __init__(self,hwnd:int): 
        self.lock=Lock()
        self.hwnd=hwnd
        # 获取窗口大小
        # 改变以解决窗口大小变小
        # 解决地址 https://stackoverflow.com/questions/3192232/getwindowrect-too-small-on-windows-7
        try:
            f = ctypes.windll.dwmapi.DwmGetWindowAttribute
        except WindowsError:
            raise Exception('size get error:{}'.format(hwnd))
        if f:
            rect = ctypes.wintypes.RECT()
            DWMWA_EXTENDED_FRAME_BOUNDS = 9
            f(ctypes.wintypes.HWND(self.hwnd),
            ctypes.wintypes.DWORD(DWMWA_EXTENDED_FRAME_BOUNDS),
            ctypes.byref(rect),
            ctypes.sizeof(rect)
            )
            self.w=rect.right - rect.left
            self.h=rect.bottom - rect.top       
            
            # print(self.w,self.h)
        
    # 获取截图
    def getScerrnShot(self):
        #获取窗口图像数据
        wDC=win32gui.GetWindowDC(self.hwnd)
        dcObj=win32ui.CreateDCFromHandle(wDC)
        cDC=dcObj.CreateCompatibleDC()
        dataBitMap=win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj,self.w,self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0,0),(self.w,self.h),dcObj,(0,0),win32con.SRCCOPY)
        
        # 保存屏幕截图
        # dataBitMap.SaveBitmapFile(cDC,'debug.bmp')
        # 返回图片的获取
        sigenedIntsArray=dataBitMap.GetBitmapBits(True)
        img=np.fromstring(sigenedIntsArray,dtype='uint8')
        img.shape=(self.h,self.w,4)
        
        # 释放资源
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd,wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle()) 
        
        # 删除图片的alpha通道 否则模板匹配的时候会报错
        img=img[...,:3]
        
        img=np.ascontiguousarray(img)
        
        # 转灰度图
        img=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
        
        return img[39:,10:1282]
    
     # 线程方法
    def start(self):
        if self.stopped:
            self.stopped=False
            t=Thread(target=self.run)
            t.start()
    # 停止线程
    def stop(self):
        self.stopped=True
    # run 方法
    def run(self):
        while not self.stopped:
            img=self.getScerrnShot()
            # 这里的锁只锁变量，别锁方法 锁方法把方法里的变量也都锁了
            self.lock.acquire()
            self.img=img
            self.lock.release()
         



