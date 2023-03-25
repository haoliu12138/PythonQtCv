from turtle import down
import win32gui,win32ui,win32con,win32api
from time import sleep
from keydict import VK_CODE
from enum import Enum
class Direction(Enum):
    up='w'
    down='s'
    left='a'
    right='d'
# 点击虚拟键盘，这里需要先定位到对应窗口
# 参数分别为点击的按键和延时时间
def click(key,time):
    # 用sendmessage 不会松开按键
    # 解决方案地址 gist.github.com/chriskieh/2906125
    win32api.keybd_event(VK_CODE[key],0,0,0)
    sleep(time)
    win32api.keybd_event(VK_CODE[key],0,win32con.KEYEVENTF_KEYUP,0)
# 移动函数
# 指定方向移动指定距离
def move(direction,distince):
    if direction!=Direction.up and direction!=Direction.down and direction!=Direction.left and direction!=Direction.right:
        raise Exception('移动方向参数并非枚举值内的上下左右值')
    click(direction.value,distince*0.25)
       
            

    
            