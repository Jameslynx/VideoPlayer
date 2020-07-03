"""
###############################################################################
# player.py: 
# PyQt5 Video and Audio Player; Independent usage by running file as main;
# Also Embeded usage in another PyQt5 QWidget or QMainWindow;
    # ################################
    # # Key Shortcuts:               #
    # #  S: Stop                     #
    # #  Left: Rewind                #
    # #  Right: Forward              #
    # #  M: toggle mute              #
    # #  Up: plus volume             #
    # #  L: toggle repeat            #
    # #  Down: minus volume          #
    # #  F: toggle fullscreen        #
    # #  Space: Play and Pause       #
    # #  Ctrl+O: Open Media file     #
    # ################################
###############################################################################
"""

###############################################################################
# TO DO: cd support
# TO Do: All video formats support (mpg)
###############################################################################

import os
import time
from PyQt5.QtGui import (
    QIcon, QFont, QPalette, QPixmap, QKeySequence)
from PyQt5.QtCore import QDir, Qt, QUrl, QSize
from PyQt5.QtMultimedia import (
    QMediaContent, QMediaPlayer, QMediaResource)
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (
    QApplication, QFileDialog, QHBoxLayout,
    QLabel, QSizePolicy, QStyle, QVBoxLayout,
    QWidget, QStatusBar, QShortcut)

try:
    from .buttons import Button
    from .qslider import VolumeSlider, PositionSlider    # Custom Sliders
    from .style import stylesheet                        # Position Slider styling
except ImportError:
    from buttons import Button
    from qslider import VolumeSlider, PositionSlider    # Custom Sliders
    from style import stylesheet                        # Position Slider styling


FOLDER = os.path.dirname(__file__)

class Player(QWidget):
    """Sub-class of QWidget"""

    def __init__(self, parent=None, *args, **kwargs):
        """Initialize class attributes"""
        super(Player, self).__init__(parent, *args, **kwargs)
        self.init_ui()

    def init_ui(self):
        """Create local components"""
        # loop
        self.loop = False
        # time label text
        self.time_text = '{:0>2d}:{:0>2d}:{:0>2d}/{:0>2d}:{:0>2d}:{:0>2d}'
        self.hours = self.minutes = self.seconds = 0
        # create media player object
        self.mediaPlayer = QMediaPlayer(self, QMediaPlayer.VideoSurface)
        # create videowidget object
        self.videoWidget = QVideoWidget()

        # create open button
        self.btn_size = QSize(16, 16)
        openButton = Button("Open")
        openButton.setToolTip("Open Media File")
        openButton.setStatusTip("Open Media File")
        openButton.setFixedHeight(24)
        openButton.setIconSize(self.btn_size)
        openButton.setIcon(QIcon.fromTheme("document-open", QIcon("Icons/Open.bmp")))
        # openButton.setStyleSheet("background-color: #B0C4DE")
        openButton.clicked.connect(self.abrir)
    
        # create play button
        self.playButton = Button()
        self.playButton.setEnabled(False)
        self.playButton.setFixedHeight(24)
        self.playButton.setIconSize(self.btn_size)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        # self.playButton.setStyleSheet("background-color: #B0C4DE")
        self.playButton.clicked.connect(self.play)

        # create slider
        self.positionSlider = PositionSlider(self.mediaPlayer, Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.setObjectName("positionSlider")
        
        # create status bar
        self.statusBar = QStatusBar()
        self.statusBar.setFont(QFont("Noto sans", 8))
        self.statusBar.setFixedHeight(14)
        self.statusBar.setStyleSheet('color:#ffffff')

        # create duration time label
        self.durationLabel = QLabel()
        self.durationLabel.setStyleSheet('background-color:rgba(255, 255, 255, 0)')
        self.durationLabel.setText('00:00:00/00:00:00')

        # create hbox layout
        controlLayoutWidget = QWidget(self)
        controlLayout = QHBoxLayout(controlLayoutWidget)
        controlLayoutWidget.setLayout(controlLayout)
        controlLayout.setContentsMargins(2, 2, 2, 2)
        # set widgets to the hbox layout
        controlLayout.addWidget(openButton)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.positionSlider)
        controlLayout.addWidget(self.durationLabel)
        # change hbox color
        controlLayoutWidget.setStyleSheet('background-color:rgba(255, 255, 255, 50)')
        controlLayoutWidget.setWindowOpacity(0.1)
        
        # create vbox layout
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        # set widgets to vbox layout
        self.layout.addWidget(self.videoWidget)
        self.layout.addWidget(controlLayoutWidget)
        self.sub_controls()
        self.layout.addWidget(self.statusBar)
        
        self.setLayout(self.layout)

        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)
        self.statusBar.showMessage('{:->33s}{:-<33s}'.format("Have Fun", ""))
        self.key_bindings()

    def key_bindings(self):
        # bind Keys to methods
        self.onplaypause = self.create_shortcut(Qt.Key_Space,
                                                self.videoWidget,
                                                self.play)                  # Space key for

        self.on_fscreen = self.create_shortcut(Qt.Key_F,
                                               self.videoWidget,
                                               self.toggle_fullscreen)      # F key for fullscreen on

        self.onforward = self.create_shortcut(Qt.Key_Right,
                                              self.videoWidget,
                                              self.forward)         # Right key for forward

        self.redvolume = self.create_shortcut(Qt.Key_Down,
                                             self.videoWidget,
                                             self.red_volume)       # Down key reduce volume

        self.incvolume = self.create_shortcut(Qt.Key_Up,
                                              self.videoWidget,
                                              self.inc_volume)      # Up key increase volume

        self.onsetloop = self.create_shortcut("L",
                                              self.videoWidget,     # L key for repeat on,
                                              (lambda self=self: 
                                               self.repeat.toggle() or
                                               self.play_again()))
        
        self.onrewind = self.create_shortcut(Qt.Key_Left,
                                             self.videoWidget,
                                             self.rewind)           # Left key for rewind

        self.volmute = self.create_shortcut(Qt.Key_M,
                                            self.videoWidget,
                                            self.mute)              # M for mute and unmute
            
        self.onopen = self.create_shortcut('Ctrl+O',
                                           self.videoWidget,
                                           self.abrir)              # Ctrl+O for open

        self.onstop = self.create_shortcut(Qt.Key_S,
                                           self.videoWidget,
                                           self.stop_media)         # S key for stop

    def create_shortcut(self, sequence, widget, obj):
        """generate key shortcuts"""
        return QShortcut(
            QKeySequence(sequence),
            widget,
            obj,
            context=Qt.ApplicationShortcut)

    def sub_controls(self):
        """Repeat, volume, and mute controls"""
        # repeat button
        self.repeat = Button()
        self.repeat.setCheckable(True)
        self.repeat.toggle()
        self.repeat.setIconSize(self.btn_size)
        self.repeat.setFixedHeight(24)
        self.repeat.setFixedWidth(26)
        self.repeat.setToolTip("repeat")
        self.repeat.setStatusTip("repeat")

        # Icons to correspond with button state
        icon = QIcon()
        icon.addPixmap(
            QPixmap(os.path.join(
                FOLDER, "Icons/repeat(1).png")),
                QIcon.Normal, QIcon.On)
        icon.addPixmap(
            QPixmap(os.path.join(
                FOLDER, "Icons/repeat(2).png")),
                QIcon.Active)
        self.repeat.setIcon(icon)
        # self.repeat.setStyleSheet("background-color: #B0C4DE; margin: 0px 0px 0px 2px;")
        self.repeat.clicked.connect(self.play_again)

        # stop button
        self.stop = Button()
        self.stop.setIconSize(self.btn_size)
        self.stop.setFixedHeight(24)
        self.stop.setFixedWidth(26)
        self.stop.setToolTip("Stop playing media")
        self.stop.setStatusTip("Stop playing media")
        self.stop.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        # self.stop.setStyleSheet("background-color: #B0C4DE; margin: 0px 0px 0px 2px;")
        self.stop.clicked.connect(self.stop_media)

        # volume slider
        self.volumeSlider = VolumeSlider(self.mediaPlayer, Qt.Horizontal)
        self.volumeSlider.setRange(0, 100)
        self.volumeSlider.setFixedWidth(200)
        self.mediaPlayer.setVolume(50)
        self.volumeSlider.sliderMoved.connect(self.set_volume)

        # volume button
        self.volume = Button(self)
        self.volume.setIconSize(self.btn_size)
        self.volume.setFixedHeight(24)
        self.volume.setFixedWidth(26)
        self.volume.setToolTip("Mute or Unmute")
        self.volume.setStatusTip("Mute or Unmute")
        self.volume.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))
        # self.volume.setStyleSheet("background-color: #B0C4DE; margin: 0px 0px 0px 2px;")
        self.volume.clicked.connect(self.mute)


        # create control widget
        subControlWidget = QWidget(self)
        subControlWidget.setStyleSheet('background-color:rgba(255, 255, 255, 30)')
        # create Horizontal Layout
        subControlLayout = QHBoxLayout(subControlWidget)
        subControlLayout.setContentsMargins(0, 0, 0, 0)
        subControlLayout.addWidget(self.repeat, 0, Qt.AlignLeft)
        subControlLayout.addWidget(self.stop, 1, Qt.AlignLeft)
        # sub layout for volume control
        self.sub_layout = QHBoxLayout()
        self.sub_layout.addWidget(self.volume)
        self.sub_layout.addWidget(self.volumeSlider)
        subControlLayout.addLayout(self.sub_layout)
        subControlLayout.setContentsMargins(2, 2, 2, 2)

        self.layout.addWidget(subControlWidget)


    def abrir(self, event=None, url=None):
        """" Equivalent to open for most GUIs"""
        fileName = None
        if self.videoWidget.isFullScreen():
            self.toggle_fullscreen()
        if not url:
            fileName, _ = QFileDialog.getOpenFileName(self, "Select media")
            if fileName:
                self.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(fileName))) 
        else:
            self.mediaPlayer.setMedia(
                    QMediaContent(QUrl(url)))
        if url or fileName:
            self.volumeSlider.setValue(self.mediaPlayer.volume())
            self.playButton.setEnabled(True)
            self.statusBar.showMessage((fileName or url))
            if not self.loop:
                self.play()

    def play(self):
        """Start media player"""
        if self.playButton.isEnabled():
            if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
                self.mediaPlayer.pause()
            else:
                self.mediaPlayer.play()

    def mediaStateChanged(self, state):
        """Callback for media player state change"""
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay))
        if state == QMediaPlayer.StoppedState and self.loop:
            self.play()

    def positionChanged(self, position):
        """Callback for media player position change"""
        if self.mediaPlayer.state() == QMediaPlayer.StoppedState:
            position = 0
        self.positionSlider.setValue(position)
        hours, position = position // 3600000, position % 3600000
        minutes, position = position // 60000, position % 60000
        seconds = position // 1000
        self.durationLabel.setText(self.time_text.format(
                                        hours, minutes, seconds, self.hours,
                                        self.minutes, self.seconds))

    def durationChanged(self, duration):
        """Callback for media player duration of media change"""
        self.positionSlider.setRange(0, duration)
        self.hours, duration = duration // 3600000, duration % 3600000
        self.minutes, duration = duration // 60000, duration % 60000
        self.seconds = duration // 1000
        self.durationLabel.setText(self.time_text.format(
                                        0, 0, 0, self.hours,
                                        self.minutes, self.seconds))

    def setPosition(self, position):
        """set media player play position"""
        self.mediaPlayer.setPosition(position)
    
    def handleError(self):
        """Callback for multiplayer errors"""
        self.playButton.setEnabled(False)
        self.statusBar.showMessage("Error: " + self.mediaPlayer.errorString())

    def play_again(self):
        """Set repeat on or off"""
        self.loop = not self.loop

    def stop_media(self):
        """Callback for stop button"""
        if self.loop:
            self.loop = False
            self.repeat.toggle()
        self.mediaPlayer.stop()

    def toggle_fullscreen(self):
        """Toggle in or out of fullscreen mode"""
        self.videoWidget.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint)
        if self.videoWidget.isFullScreen():
            self.videoWidget.setFullScreen(False)
            self.videoWidget.setWindowState(Qt.WindowNoState)
            self.videoWidget.setParent(self)
            self.layout.insertWidget(0, self.videoWidget)
            self.videoWidget.showNormal()
            self.show()
        else:
            self.videoWidget.setFullScreen(True)
            self.hide()

    def rewind(self, lapse=2500):
        """Rewind the current media file by 1 second"""
        new_position = self.mediaPlayer.position() - lapse
        self.setPosition(new_position)

    def forward(self, lapse=2500):
        """Forward media file by 1 second"""
        new_position = self.mediaPlayer.position() + lapse
        self.setPosition(new_position)

    def set_volume(self, vol=0):
        """Set media player volume volume"""
        if vol:
            self.mediaPlayer.setVolume(vol)

    def red_volume(self, vol=1):
        """Reduce volume by a factor of 0.01"""
        volume = self.mediaPlayer.volume()
        if volume >= 0:
            new_volume = volume - 1
            self.volumeSlider.setValue(new_volume)
            self.set_volume(new_volume)

    def inc_volume(self, vol=1):
        """Increase volume by a factor of 0.01"""
        volume = self.mediaPlayer.volume()
        if self.mediaPlayer.isMuted():
            self.mediaPlayer.setMuted(False)
            self.volume.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))
        if volume <= 100:
            new_volume = volume + 1
            self.volumeSlider.setValue(new_volume)
            self.set_volume(new_volume)

    def mute(self):
        """Mute media player"""
        if self.mediaPlayer.isMuted():
            self.mediaPlayer.setMuted(False)
            self.volume.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))
        else:
            self.mediaPlayer.setMuted(True)
            self.volume.setIcon(self.style().standardIcon(QStyle.SP_MediaVolumeMuted))

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(os.path.join(FOLDER, 'Icons/icon.png')))
    app.setStyleSheet(stylesheet)
    player = Player()
    p = player.palette()
    p.setColor(QPalette.Window, Qt.black)   # set background color
    player.setPalette(p)
    player.show()
    sys.exit(app.exec_())
