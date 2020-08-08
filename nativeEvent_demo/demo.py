from ctypes.wintypes import POINT
import ctypes.wintypes

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton
from PyQt5.QtWinExtras import QtWin
import win32api
import win32con
import win32gui



class MINMAXINFO(ctypes.Structure):
    _fields_ = [
        ("ptReserved",      POINT),
        ("ptMaxSize",       POINT),
        ("ptMaxPosition",   POINT),
        ("ptMinTrackSize",  POINT),
        ("ptMaxTrackSize",  POINT),
    ]


class Window(QWidget):

    BorderWidth = 5

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        # 主屏幕的可用大小（去掉任务栏）
        self._rect = QApplication.instance().desktop().availableGeometry(self)
        self.resize(800, 600)
        self.setWindowFlags(Qt.Window
                            | Qt.FramelessWindowHint
                            | Qt.WindowSystemMenuHint
                            | Qt.WindowMinimizeButtonHint
                            | Qt.WindowMaximizeButtonHint
                            | Qt.WindowCloseButtonHint)
        # 增加薄边框
        style = win32gui.GetWindowLong(int(self.winId()), win32con.GWL_STYLE)
        win32gui.SetWindowLong(
            int(self.winId()), win32con.GWL_STYLE, style | win32con.WS_THICKFRAME)

        if QtWin.isCompositionEnabled():
            # 加上 Aero 边框阴影
            QtWin.extendFrameIntoClientArea(self, -1, -1, -1, -1)
        else:
            QtWin.resetExtendedFrame(self)

    def nativeEvent(self, eventType, message):
        retval, result = super(Window, self).nativeEvent(eventType, message)
        if eventType == "windows_generic_MSG":
            msg = ctypes.wintypes.MSG.from_address(message.__int__())
            # 获取鼠标移动经过时的坐标
            x = win32api.LOWORD(msg.lParam) - self.frameGeometry().x()
            y = win32api.HIWORD(msg.lParam) - self.frameGeometry().y()
            # 判断鼠标位置是否有其它控件
            if self.childAt(x, y) != None:
                return retval, result
            if msg.message == win32con.WM_NCCALCSIZE:
                # 拦截不显示顶部的系统自带的边框
                return True, 0
            if msg.message == win32con.WM_GETMINMAXINFO:
                # 当窗口位置改变或者大小改变时会触发该消息
                info = ctypes.cast(
                    msg.lParam, ctypes.POINTER(MINMAXINFO)).contents
                print(info)
                # 修改最大化的窗口大小为主屏幕的可用大小
                info.ptMaxSize.x = self._rect.width()
                info.ptMaxSize.y = self._rect.height()
                # 修改放置点的x,y坐标为0,0
                info.ptMaxPosition.x, info.ptMaxPosition.y = 0, 0
            if msg.message == win32con.WM_NCHITTEST:
                w, h = self.width(), self.height()
                lx = x < self.BorderWidth
                rx = x > w - self.BorderWidth
                ty = y < self.BorderWidth
                by = y > h - self.BorderWidth
                # 左上角
                if (lx and ty):
                    return True, win32con.HTTOPLEFT
                # 右下角
                if (rx and by):
                    return True, win32con.HTBOTTOMRIGHT
                # 右上角
                if (rx and ty):
                    return True, win32con.HTTOPRIGHT
                # 左下角
                if (lx and by):
                    return True, win32con.HTBOTTOMLEFT
                # 上
                if ty:
                    return True, win32con.HTTOP
                # 下
                if by:
                    return True, win32con.HTBOTTOM
                # 左
                if lx:
                    return True, win32con.HTLEFT
                # 右
                if rx:
                    return True, win32con.HTRIGHT
                # 标题
                return True, win32con.HTCAPTION
        return retval, result


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = Window()
    btn = QPushButton('exit', w, clicked=app.quit)
    btn.setGeometry(10, 10, 100, 40)
    w.show()
    sys.exit(app.exec_())