import sys

from PyQt5.QtCore import QEvent, QSize, Qt, QPoint
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QAction, QApplication, QHBoxLayout, QLabel, QMenu, QPushButton,
    QVBoxLayout, QWidget)

from album_cover_viewer import AlbumCardViewer


class AlbumTabInterface(QWidget):
    """ 定义专辑卡标签界面 """

    def __init__(self, target_path, parent=None):
        super().__init__(parent)
        self.resize(1267, 684)

        # 实例化专辑视图
        self.albumViewer = AlbumCardViewer(target_path)

        # 实例化无序播放所有按钮
        self.randomPlayBt = QPushButton(
            QIcon('resource\\images\\无序播放所有_130_17.png'), '', self)
        self.randomPlayBt.setIconSize(QSize(130, 17))

        # 实例化排序依据标签、按钮和菜单
        self.sortModeMenu = QMenu(self)
        self.sortModeLabel = QLabel('排序依据:', self)
        self.sortModeButton = QPushButton('添加日期', self)

        # 实例化布局
        self.h_layout = QHBoxLayout()
        self.all_v_layout = QVBoxLayout()

        # 将动作添加到菜单中
        self.addActionToMenu()

        # 设置初始排序方式
        self.currentSortMode = self.sortByCratedTime
        self.sortModeNum_dict = {'添加日期': 0, 'A到Z': 1, '发行年份': 2, '歌手': 3}
        # 初始化UI界面
        self.initWidget()
        self.initLayout()
        self.setQss()

    def initWidget(self):
        """ 初始化小部件 """

        # 获取专辑总数
        albums_num = len(self.albumViewer.albumCardDict_list)
        self.randomPlayBt.setText(f'({albums_num})')

        # 设置鼠标光标
        self.sortModeButton.setCursor(Qt.PointingHandCursor)
        self.randomPlayBt.setCursor(Qt.PointingHandCursor)

        # 分配ID
        self.setObjectName('albumTabInterface')
        self.sortModeMenu.setObjectName('sortModeMenu')
        self.sortModeLabel.setObjectName('sortModeLabel')
        self.sortModeButton.setObjectName('sortModeButton')
        self.randomPlayBt.setObjectName('randomPlayBt')

        # 将信号连接到槽函数
        self.randomPlayBt.clicked.connect(self.changeLoopMode)
        self.sortModeButton.clicked.connect(self.showSortModeMenu)

        # 给loopModeButton设置监听
        self.randomPlayBt.installEventFilter(self)

    def initLayout(self):
        """ 初始化布局 """

        self.h_layout.addWidget(self.randomPlayBt, 0, Qt.AlignLeft)
        self.h_layout.addSpacing(38)
        self.h_layout.addWidget(self.sortModeLabel, 0, Qt.AlignLeft)
        self.h_layout.addWidget(self.sortModeButton, 0, Qt.AlignLeft)
        # 不给按钮和标签分配多余的空间
        self.h_layout.addStretch(1)

        self.all_v_layout.addSpacing(7)
        self.all_v_layout.addLayout(self.h_layout)
        self.all_v_layout.addSpacing(0)
        self.all_v_layout.addWidget(self.albumViewer)
        self.setLayout(self.all_v_layout)

    def addActionToMenu(self):
        """ 将动作添加到菜单里 """

        # 创建排序列表项目的动作
        self.sortByDictOrder = QAction(
            'A到Z', self, triggered=self.sortAlbumCard)
        self.sortByCratedTime = QAction(
            '添加日期', self, triggered=self.sortAlbumCard)
        self.sortByYear = QAction('发行年份', self, triggered=self.sortAlbumCard)
        self.sortBySonger = QAction('歌手', self, triggered=self.sortAlbumCard)
        # 设置动作的悬浮提醒
        self.sortByCratedTime.setToolTip('添加时间')
        self.sortByDictOrder.setToolTip('A到Z')
        self.sortByYear.setToolTip('发行年份')
        self.sortBySonger.setToolTip('歌手')

        # 将动作添加到菜单中
        self.sortModeMenu.addActions(
            [self.sortByCratedTime, self.sortByDictOrder, self.sortByYear, self.sortBySonger])

    def changeLoopMode(self):
        """ 改变播放的循环模式 """
        pass

    def sortAlbumCard(self):
        """ 根据所选的排序方式对歌曲卡进行重新排序 """
        sender = self.sender()
        self.currentSortMode = sender
        # 清空旧的列表

        # 更新分组
        if sender == self.sortByCratedTime and self.albumViewer.sortMode != '添加时间':
            self.sortModeButton.setText('添加时间')
            self.albumViewer.update()
            self.albumViewer.createAddTimeGroup()
        elif sender == self.sortByDictOrder:
            self.sortModeButton.setText('A到Z')
            self.albumViewer.sortMode = 'A到Z'
            self.albumViewer.createFirstLetterGroup()
            self.albumViewer.sortByFirsetLetter()
        elif sender == self.sortByYear:
            self.sortModeButton.setText('发行年份')
        elif sender == self.sortBySonger:
            self.sortModeButton.setText('歌手')

    def showSortModeMenu(self):
        """ 显示排序方式菜单 """
        # 设置默认动作
        self.sortModeMenu.setDefaultAction(self.currentSortMode)
        self.sortModeMenu.exec(
            self.mapToGlobal(QPoint(self.sortModeButton.x(),
                                    self.sortModeButton.y() - 37*self.sortModeNum_dict[self.currentSortMode.text()]-1)))

    def setQss(self):
        """ 设置层叠样式 """
        with open('resource\\css\\albumTabInterface.qss', 'r', encoding='utf-8') as f:
            qss = f.read()
            self.setStyleSheet(qss)

    def eventFilter(self, obj, event):
        """ 当鼠标移到播放模式按钮上时更换图标 """
        if obj == self.randomPlayBt:
            if event.type() == QEvent.Enter or event.type() == QEvent.HoverMove:
                self.randomPlayBt.setIcon(
                    QIcon('resource\\images\\无序播放所有_hover_130_17.png'))
            elif event.type() == QEvent.Leave:
                self.randomPlayBt.setIcon(
                    QIcon('resource\\images\\无序播放所有_130_17.png'))

        return False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = AlbumTabInterface('D:\\KuGou')
    demo.show()
    sys.exit(app.exec_())