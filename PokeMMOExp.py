import sys
from PySide6 import QtWidgets
from mainWin import MainWin
if __name__=="__main__":
    app=QtWidgets.QApplication(sys.argv)
    
    win=MainWin()
    win.show()
    
    sys.exit(app.exec())