from threading import Thread,Lock
import cv2 as cv 
from windowsCapture import WindowCapture 
from detection import Detection
import botOperation
import time
class ExpAuto:
    def __init__(self,hwnd):
        self.hwnd=hwnd
        self.stopped=True
        # 加载屏幕捕获器
        self.wincap=WindowCapture(hwnd)
        # 启动屏幕捕获器
        self.wincap.start()
        # 加载检测器 精灵中心外
        self.centerout=Detection('Photos\CenterOut.png',0.8)
        self.centerout.start()
        # 加载检测器 精灵中心医生处
        self.centerin=Detection('Photos\CenterIn.png',0.8)
        self.centerin.start()
        # 加载检测器 门口
        self.bd=Detection('Photos\Black.png',0.8)
        self.bd.start()
        # 加载检测器 马场
        self.hourse=Detection('Photos\hourse.png',0.8)
        self.hourse.start()
        
                
    def start(self):
        self.stopped=False
        t=Thread(target=self.run)
        t.start()
        
    def stop(self):
        self.stopped=True
    # 进入精灵中心并且走出的操作
    def into_center(self):
        while True:
            if self.wincap.img is not None:
                self.centerout.update_check(self.wincap.img)
                if self.centerout.result==True:
                    # 检测到某个位置执行操作前需要关闭当前线程，否则会出现一个操作执行两遍的情况
                    print('位于精灵中心门口')
                    print('进入精灵中心')
                    botOperation.move(botOperation.Direction.up,1) 
                    while True:
                        # 这个必须啊一直更新这个图片否则这个会出现问题
                        self.centerout.update_check(self.wincap.img)
                        self.centerin.update_check(self.wincap.img)
                        # 向前移动
                        botOperation.move(botOperation.Direction.up,1) 
                        if self.centerin.result==True:
                            print('位于医生处')
                            botOperation.click('u',5)
                            print('等待医生处理')
                            botOperation.click('u',1)
                            print('处理结束')
                            botOperation.move(botOperation.Direction.down,8)
                            time.sleep(3)
                            print('走出精灵中心')
                            
                            return
                            
                            
   
                
            
    # 走向马场 
    def go_hourse(self):
        print('走向马场')
        botOperation.move(botOperation.Direction.left,36)
        # botOperation.move(botOperation.Direction.up,0.25)
        
        botOperation.click('2',0.25)
        botOperation.click('d',0.1)
        botOperation.click('u',0.25)
        time.sleep(5)
        botOperation.click('w',0.25)
        
        
        
        
    def run(self):
        while not self.stopped:
            self.into_center()
            self.go_hourse()
            
        
            
                            
            