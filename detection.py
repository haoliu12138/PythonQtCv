import cv2 as cv
import os
from threading import Thread,Lock
import time
import numpy
class Detection:
    # 锁对象
    lock=None
    # 模板图像
    template=None
    # 检测图片
    check=None
    # 模板宽高
    tmp_w=0
    tmp_h=0
    # 检测出来的矩形坐标
    topleft=(0,0)
    rightbutton=(0,0)
    # 多少值才算匹配到
    resval=1
    # 检测结果
    result=False
    # 结果值
    maxval=0
    # 线程状态
    stopped=True
    # 构造函数self要写在前面
    def __init__(self,path:str,resval:float):
        self.lock=Lock()
        self.resval=resval
        # 读取模板
        self.template=cv.imread(path,cv.IMREAD_GRAYSCALE)
        # 获取模板宽高
        self.tmp_h,self.tmp_w=self.template.shape
    # 检测方法
    def detect(self):
        res=cv.matchTemplate(self.check,self.template,cv.TM_CCOEFF_NORMED)
        # 匹配度到预设的值
        minval,maxval,minloc,maxloc=cv.minMaxLoc(res)
        if maxval>self.resval:
            topleft=maxloc
            rightbutton=(maxloc[0]+self.tmp_w,maxloc[1]+self.tmp_h)
            result=True;
        else:
            topleft=(-1,-1)
            rightbutton=(-1,-1)
            result=False;
        return maxval,result,topleft,rightbutton
    # 更新检测图片的方法
    def update_check(self,check):
        self.lock.acquire()
        self.check=check
        self.lock.release()
    # 线程方法
    def start(self):
        self.stopped=False
        t=Thread(target=self.run)
        t.start()
    # 停止线程
    def stop(self):
        self.lock.acquire()
        self.stopped=True
        self.result=False
        self.lock.release()
    # run 方法
    def run(self):
        while not self.stopped:
            if self.check is not None:
                maxval,result,topleft,rightbutton=self.detect()
                self.lock.acquire()
                self.maxval=maxval
                self.result=result
                self.topleft,self.rightbutton=topleft,rightbutton
                self.lock.release()
    


    
    
        
        