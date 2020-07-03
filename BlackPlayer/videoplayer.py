"""
##########################################################################
# videoplayer.py:
# Combines Player and TrailerPlayer;
# To create a multipurpose PyQt5 app to play media files;
# Play movies and Tv shows previews;
# Icons:
    # <a target="_blank" href="https://icons8.com/icons/set/streaming-media">
    #   Streaming Media icon</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
    # <a target="_blank" href="https://icons8.com/icons/set/preview-pane">Preview Pane icon</a>
    #   icon by <a target="_blank" href="https://icons8.com">Icons8</a>
    # <a target="_blank" href="https://icons8.com/icons/set/video">Video icon</a>
    #   icon by <a target="_blank" href="https://icons8.com">Icons8</a>
    # <div>Icons made by <a href="https://www.flaticon.com/authors/freepik" title="Freepik">Freepik</a>
    #   from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
##########################################################################
"""
import os
import json
import pyautogui 
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from .buttons import TransitionButton
from .player import Player
from .trailer import TrailerPlayer
from .style import stylesheet

FOLDER = os.path.dirname(__file__)              # file's parent folder

pyautogui.FAILSAFE = False

class MainPlayer(QWidget):
    """Sub-class of QWidget"""

    def __init__(self, parent=None):
        """initialize class attributes"""
        super(MainPlayer, self).__init__(parent)
        self.setWindowTitle("BlackPlayer")
        self.setMinimumSize(560, 480)
        p = self.palette()
        p.setColor(QPalette.Window, Qt.black)   # set background color
        self.setPalette(p)
        self.init_ui()

    def init_ui(self):
        """create widget components"""
        # transition buttons
        self.p_button = TransitionButton()
        self.t_button = TransitionButton()
        self.p_button.setText("Player")
        self.t_button.setText("Previews")
        self.p_button.setToolTip("Go to player")
        self.p_button.setStatusTip("Go to player")
        self.t_button.setToolTip("Go to trailers")
        self.t_button.setStatusTip("Go to trailers")
        self.p_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.t_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.p_button.clicked.connect(lambda : self.display(i=0))
        self.t_button.clicked.connect(lambda : self.display(i=1))

        self.player = Player(self)
        self.tlayer = TrailerPlayer(self)
        self.p_button.setIconSize(self.player.btn_size)
        self.t_button.setIconSize(self.tlayer.btn_size)
        self.p_button.setIcon(QIcon(os.path.join(FOLDER, 'Icons/video-24.png')))
        self.t_button.setIcon(QIcon(os.path.join(FOLDER, 'Icons/preview-pane-24.png')))
        self.player.sub_layout.addWidget(self.t_button)
        self.tlayer.hlayout.addWidget(self.p_button, 2)

        # create a stacked widget
        self.Stack = QStackedWidget(self)
        self.Stack.addWidget(self.player)
        self.Stack.addWidget(self.tlayer)

        # create vertical layout
        hbox = QVBoxLayout(self)
        hbox.addWidget(self.Stack)

        # set vertical layout as primary widget layout
        self.setLayout(hbox)
        QTimer.singleShot(5000, self.awake)

    def display(self, event=None, i=0):
        """Change display on transtion button click"""
        if i == 1:
            self.player.mediaPlayer.pause()
        self.Stack.setCurrentIndex(i)

    def awake(self):
        """prevent system from being idle"""
        pyautogui.press('shift') 
        QTimer.singleShot(60000, self.awake) 
            
def main():
    import sys
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(os.path.join(FOLDER, 'Icons/icon.png')))
    app.setStyleSheet(stylesheet)
    player = MainPlayer()
    player.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()