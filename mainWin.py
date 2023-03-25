from PySide6 import QtWidgets,QtCore
import  win32GuiUtil 
from expAuto import ExpAuto
import win32gui
# 主窗口类
class MainWin(QtWidgets.QWidget):
    # 构造函数中初始化窗口组件
    def __init__(self):
        super().__init__()  
        # 是否可以运行
        self.canRun=False
        
        self.setWindowTitle('PokeMMO经验脚本')
        # 文本框 用于输出日志
        self.textEdit=QtWidgets.QPlainTextEdit()
        self.textEdit.setMaximumBlockCount(100)
        self.textEdit.setReadOnly(True)
        # 布局 
        self.layout=QtWidgets.QGridLayout(self)
        # 检查按钮
        self.checkBtn=QtWidgets.QPushButton()
        self.checkBtn.setText('列出窗口名称')
        # 开始按钮
        self.startBtn=QtWidgets.QPushButton()
        self.startBtn.setText('开始运行')
        # 文本框用于输入hwnd
        self.text=QtWidgets.QLineEdit()
        self.label=QtWidgets.QLabel()
        self.label.setText('窗口句柄')
        
        
        
        self.layout.addWidget(self.checkBtn,1,1) 
        self.layout.addWidget(self.startBtn,1,2) 
        self.layout.addWidget(self.text,2,2,1,1)
        self.layout.addWidget(self.label,2,1,1,1)
        self.layout.addWidget(self.textEdit,3,1,1,2)
        
        self.resize(800,600)
        # 连接信号和槽函数
        self.checkBtn.clicked.connect(self.check)
        self.startBtn.clicked.connect(self.start)
    # 向textedit中输出日志内容
    def logPrint(self,inputStr:str):
        self.textEdit.appendPlainText(inputStr)

                          
    # 检查按钮调用槽函数
    @QtCore.Slot()
    def check(self):
        dicts=win32GuiUtil.list_window_names()
        for name in dicts.keys():
            self.logPrint(f'{name}:{dicts[name]}')
            
            
    # 开始按钮调用槽函数
    @QtCore.Slot()
    def start(self):
        self.expauto=ExpAuto(int(self.text.text()))
        if self.expauto.stopped==True:
            self.expauto.start()        
        # 定位窗口
        win32gui.SetForegroundWindow(int(self.text.text()))
        

        
        
        
        
        

        
          