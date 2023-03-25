from operator import truediv
import win32gui
import chardet
# win32gui工具类
# wine32Gui获取所有窗口句柄
def list_window_names():
    h_dict={}
    def winEnumHandler(hwnd,ctx):
        if win32gui.IsWindowVisible(hwnd):
            if(win32gui.GetWindowText(hwnd)!=''):
                h_dict[win32gui.GetWindowText(hwnd)]=hwnd          
    win32gui.EnumWindows(winEnumHandler,None)
    return h_dict
#win32Gui获取窗口以及子窗口 返回一个窗口名及句柄字典
def get_inner_windows(whndl):
    def callback(hwnd,hwnds):
        if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
            hwnds[win32gui.GetClassName(hwnd)]=hwnd
        return True
    hwnds={}
    win32gui.EnumChildWindows(whndl,callback,hwnds)
    return hwnds
