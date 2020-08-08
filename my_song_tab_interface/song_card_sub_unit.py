# coding:utf-8

""" 歌曲卡组件库 """

import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont, QFontMetrics, QIcon, QPixmap
from PyQt5.QtWidgets import (QApplication, QCheckBox, QLabel, QToolButton,
                             QWidget)


class ToolButton(QToolButton):
    """ 按钮 """

    def __init__(self, iconPath_dict: dict, parent=None):
        super().__init__(parent)
        self.iconPath_dict = iconPath_dict
        # 设置按钮状态标志位
        self.setFixedSize(60, 60)
        self.setIconSize(QSize(60, 60))
        self.setState('notSelected-notPlay')
        self.setStyleSheet("QToolButton{border:none;margin:0}")

    def setState(self, state: str):
        """ 设置按钮状态，更新按钮图标，状态有notSelected-notPlay、notSelected-play、selected这三种 """
        self.state = state
        self.setIcon(QIcon(self.iconPath_dict[state]))
        self.setProperty('state',state)

class ButtonGroup(QWidget):
    """
    按钮组, 按钮窗口的state有6种状态:
        notSelected-leave、notSelected-enter、notSelected-pressed
        selected-leave、selected-enter、selected-pressed 
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        # 创建按钮
        self.playButton = ToolButton(
            {'notSelected-notPlay': r'resource\images\song_tab_interface\黑色播放_60_60.png',
             'notSelected-play': r'resource\images\song_tab_interface\绿色播放_60_60.png',
             'selected': r'resource\images\song_tab_interface\白色播放_60_60.png'}, self)
        self.addToButton = ToolButton(
            {'notSelected-notPlay': r'resource\images\song_tab_interface\黑色添加到_60_60.png',
             'notSelected-play': r'resource\images\song_tab_interface\绿色添加到_60_60.png',
             'selected': r'resource\images\song_tab_interface\白色添加到_60_60.png'}, self)
        # 初始化
        self.__initWidget()

    def __initWidget(self):
        """ 初始化小部件 """
        self.setAttribute(Qt.WA_StyledBackground)
        self.setFixedSize(140, 60)
        # 设置按钮的绝对坐标
        self.addToButton.move(80, 0)
        self.playButton.move(20, 0)
        # 分配ID并设置属性
        self.setObjectName('buttonGroup')
        self.setProperty('state', 'notSelected-leave')
        # 隐藏按钮
        # self.setButtonHidden(True)

    def setButtonHidden(self, isHidden: bool):
        """ 设置按钮是否可见 """
        self.playButton.setHidden(isHidden)
        self.addToButton.setHidden(isHidden)

    def setButtonState(self, state: str):
        """ 根据状态更换按钮图标, 状态有notSelected-notPlay、notSelected-play、selected这三种 """
        self.playButton.setState(state)
        self.addToButton.setState(state)

    def setState(self, state: str):
        """ 设置按钮组状态 """
        self.setProperty('state', state)


class SongNameCard(QWidget):
    """ 歌名卡 """

    def __init__(self, songName, parent=None):
        super().__init__(parent)
        self.songName = songName
        self.isPlay = False
        # 创建小部件
        self.checkBox = QCheckBox(self)
        self.playingLabel = QLabel(self)
        self.songNameLabel = QLabel(songName, self)
        self.buttonGroup = ButtonGroup(self)
        self.playButton = self.buttonGroup.playButton
        self.addToButton = self.buttonGroup.addToButton
        # 初始化
        self.__initWidget()

    def __initWidget(self):
        """ 初始化小部件 """
        self.setFixedHeight(60)
        self.resize(390, 60)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.playingLabel.setPixmap(
            QPixmap(r'resource\images\song_tab_interface\绿色正在播放_16_16.png'))
        # 隐藏小部件
        self.playingLabel.hide()
        self.setWidgetHidden(True)
        # 分配属性和ID
        self.setObjectName('songNameCard')
        self.songNameLabel.setObjectName('songNameLabel')
        self.setCheckBoxBtLabelState('notSelected-notPlay')
        # 计算歌名的长度
        self.__getSongNameWidth()
        self.__initLayout()
        # self.__setQss()

    def __initLayout(self):
        """ 初始化布局 """
        self.checkBox.move(15, 18)
        self.playingLabel.move(57, 22)
        self.songNameLabel.move(57, 18)
        self.__moveButtonGroup()

    def __getSongNameWidth(self):
        """ 计算歌名的长度 """
        fontMetrics = QFontMetrics(QFont('Microsoft YaHei', 10))
        self.songNameWidth = sum([fontMetrics.width(i) for i in self.songName])

    def __moveButtonGroup(self):
        """ 移动按钮组 """
        if self.songNameWidth + self.songNameLabel.x() >= self.width() - 140:
            x = self.width() - 140
        else:
            x = self.songNameWidth + self.songNameLabel.x()
        self.buttonGroup.move(x, 0)

    def setSongName(self, songName: str):
        """ 更新歌手名标签的文本并调整宽度 """
        self.songName = songName
        self.songNameLabel.setText(songName)
        # 重新计算歌名宽度并移动按钮
        self.__getSongNameWidth()
        self.__moveButtonGroup()
        self.songNameLabel.setFixedWidth(self.songNameWidth)

    def setWidgetHidden(self, isHidden: bool):
        """ 显示/隐藏小部件 """
        self.buttonGroup.setHidden(isHidden)
        self.checkBox.setHidden(isHidden)

    def resizeEvent(self, e):
        """ 改变尺寸时移动按钮 """
        super().resizeEvent(e)
        self.__moveButtonGroup()

    def setCheckBoxBtLabelState(self, state: str):
        """ 设置复选框、按钮和标签的状态并更新样式,有notSelected-notPlay、notSelected-play、selected这3种状态 """
        self.checkBox.setProperty('state', state)
        self.songNameLabel.setProperty('state', state)
        self.buttonGroup.setButtonState(state)
        # 根据选中状态更新正在播放图标颜色
        if state == 'selected':
            self.playingLabel.setPixmap(
                QPixmap(r'resource\images\song_tab_interface\白色正在播放_16_16.png'))
        else:
            self.playingLabel.setPixmap(
                QPixmap(r'resource\images\song_tab_interface\绿色正在播放_16_16.png'))

    def setButtonGroupState(self, state: str):
        """ 设置按钮组窗口状态，按钮组状态与歌曲卡始终相同，总共6种状态 """
        self.buttonGroup.setState(state)

    def setPlay(self, isPlay: bool):
        """ 设置播放状态并决定是否显示正在播放图标 """
        self.isPlay = isPlay
        self.playingLabel.setHidden(not isPlay)
        self.setWidgetHidden(not isPlay)
        self.songNameLabel.move([57,83][isPlay], self.songNameLabel.y())
        # 更新按钮位置
        self.__moveButtonGroup()

    def setSongName(self, songName: str):
        """ 更新歌手名标签的文本并调整宽度 """
        self.songName = songName
        self.songNameLabel.setText(songName)
        # 重新计算歌名宽度并移动按钮
        self.__getSongNameWidth()
        self.__moveButtonGroup()
        self.songNameLabel.setFixedWidth(self.songNameWidth)