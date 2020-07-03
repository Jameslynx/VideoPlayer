import os
import sys
from BlackPlayer.videoplayer import MainPlayer
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from BlackPlayer.style import stylesheet


def main():
    import sys
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('BlackPlayer/Icons/icon.png'))
    app.setStyleSheet(stylesheet)
    player = MainPlayer()
    player.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()