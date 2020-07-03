"""
##############################################################################
# TrailerPlayer; Play youtube links through webview; Capable independently;
# Also embed usage in other widgets;
###############################################################################
"""
import os
import sys
import json
import time
from PyQt5.QtGui import (
    QPalette, QPixmap, QIcon,
    QCursor, QFont, QKeySequence)
from PyQt5.QtCore import (
    Qt, QUrl, QRect, QThread, QSize)
from PyQt5 import QtWebEngineCore
from PyQt5.QtWidgets import (
    QWidget, QApplication, QMainWindow,
    QVBoxLayout, QScrollArea, QLabel,
    QHBoxLayout, QGridLayout, QButtonGroup,
    QPushButton, QShortcut)
from PyQt5.QtWebEngineWidgets import *

try:
    from .dialogs import UrlDialog
    from .buttons import Button, TrailerButton
    from .Trailers.tmdb_api import Movies, TV
    from .Trailers.posters_downloader import downloader
except ImportError:
    sys.path.append(os.path.abspath(os.path.dirname(__file__)))
    from dialogs import UrlDialog
    from buttons import Button, TrailerButton
    from Trailers.tmdb_api import Movies, TV
    from Trailers.posters_downloader import downloader


YOURL = "https://www.youtube.com/watch_popup?v={}&vq=hd1080"

data_dict = {}              # movie and Tv info
trailers_dir = os.path.join(os.path.dirname(__file__), 'Trailers')  # path to Trailers folder
try:
    with open(os.path.join(trailers_dir, 'trailers.json')) as f_obj:
        data_dict = json.load(f_obj)                                # attempt to populate data
except :
    pass


class MyThread(QThread):
    """Sub-class of Qthread"""

    def __init__(self, parent=None, *args, **kwargs):
        """initialize class attributes"""
        super(MyThread, self).__init__(parent, *args, **kwargs)

    def run(self):
        """get movie_tv information"""
        global data_dict, trailers_dir
        try:
            movies = Movies()
            tv = TV()
            movies.info_populate()
            tv.info_populate()
        except:
            pass
        else:
            all_trailers = {"movies": movies.info_dict, "tv": tv.info_dict}
            with open(os.path.join(trailers_dir, 'trailers.json'), 'w') as f_obj:
                json.dump(all_trailers, f_obj, sort_keys=True, indent=4)
            downloader()
            with open(os.path.join(trailers_dir, 'trailers.json')) as f_obj:
                data_dict = json.load(f_obj)


class TrailerPlayer(QWidget):
    """Sub-class of the QWidget class"""

    def __init__(self, parent=None, *args, **kwargs):
        """Initialize class attributes"""
        super(TrailerPlayer, self).__init__()
        self.disabled = None            # Video button clicked
        self.scroll = None              # scroll area
        self.init_ui()
        self.refresh()

    def init_ui(self):
        """Create local components"""
        self.glayout = QGridLayout()        # main Grid Layout
        self.vlayout = QVBoxLayout()        # WebView Layout
        self.hlayout = QHBoxLayout()        # additional buttons 
        self.webview = QWebEngineView()     # WebView object
        self.webview.load(QUrl("http://www.youtube.com/embed/hI9GyhX7yHM?rel"
                               "=0&modestbranding=0&autohide=1&mute=0&showinfo"
                               "=0&controls=1&autoplay=1"))    # default url
        # refresh button
        self.btn_size = QSize(16, 16)
        refresh = Button()
        refresh.setEnabled(False)
        refresh.setFixedWidth(24)
        refresh.setToolTip('Refresh')
        refresh.setStatusTip('Refresh')
        icon = QIcon()
        path = os.path.join(os.path.dirname(__file__), "Icons")
        icon.addPixmap(
            QPixmap(os.path.join(path, "refresh-24.png"))
            )
        icon.addPixmap(
            QPixmap(os.path.join(path, "cancel-24.png")),
            QIcon.Disabled)
        refresh.setIcon(icon)
        refresh.clicked.connect(self.refresh)
        refresh.setCursor(QCursor(Qt.PointingHandCursor))
        self.rfresh = refresh

        # Stream button
        stream = Button()
        stream.setFixedWidth(24)
        stream.setToolTip("Stream video")
        stream.setStatusTip("Stream video")
        stream.setIconSize(self.btn_size)
        stream.setIcon(QIcon(os.path.join(path, 'streaming-media-30.png')))
        stream.clicked.connect(self.search)
        stream.setCursor(QCursor(Qt.PointingHandCursor))


        btns_widget = QWidget()
        self.hlayout.addWidget(self.rfresh, 0)
        self.hlayout.addWidget(stream, 1)
        btns_widget.setLayout(self.hlayout)
        btns_widget.setFixedWidth(330)

        self.vlayout.addWidget(self.webview)
        self.vlayout.setAlignment(Qt.AlignTop)
        self.setLayout(self.glayout)
        self.glayout.addLayout(self.vlayout, 0, 0)
        self.add_scroll_box()
        self.glayout.addWidget(btns_widget, 1, 1)
        QShortcut(
            QKeySequence(Qt.Key_Space),     # Space key responds to None
            self,
            lambda : None,
            context=Qt.ApplicationShortcut
        )

    def refresh(self):
        """refrsh movie information"""
        self.rfresh.setEnabled(False)
        thread = MyThread(self)
        thread.finished.connect(self.add_scroll_box)
        thread.start()
        

    def add_scroll_box(self):
        """Create Scroll area and its components"""
        if self.scroll:
            self.disabled = None
            self.scroll.setParent(None)
            self.rfresh.setEnabled(True)

        self.scroll = QScrollArea()             # Scroll Area which contains the widgets, set as the centralWidget
        self.widget = QWidget()                 # Widget that contains the collection of Vertical Box
        self.vbox = QVBoxLayout()               # The Vertical Box that contains the Horizontal Boxes of  labels and buttons
        self.labels_buttons()
        self.vbox.setAlignment(Qt.AlignVCenter)
        self.widget.setLayout(self.vbox)

        # Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        self.scroll.setStyleSheet('background-color:rgba(0, 0, 0, 0)')
        self.scroll.setFixedWidth(330)
        self.glayout.addWidget(self.scroll, 0, 1)

    def labels_buttons(self):
        """Create labels and buttons"""
        posters_dir = os.path.join(trailers_dir, 'posters')
        clearing = []
        for type_ in data_dict.values():
            for cat in type_.values():
                for single in cat:
                    path = os.path.join(posters_dir, single['poster'].split('/')[-1])
                    if single['title'] not in clearing:
                        self.labels(path, single)
                        clearing.append(single['title'])


    def labels(self, path, single):
        """Create labels"""
        if os.path.exists(path):
            widget = QWidget()
            v_box = QVBoxLayout()
            image = QPixmap(path)
            imageLabel = QLabel(parent=widget)
            imageLabel.setPixmap(image)
            imageLabel.setGeometry(0, 0, image.width(), image.height())
            v_box.addWidget(imageLabel)
            v_box.setAlignment(Qt.AlignVCenter)
            widget.setLayout(v_box)
            widget.setStyleSheet('background-color:rgba(255, 255, 255, 50)')
            widget.setFixedWidth(image.width())
            self.vbox.addWidget(widget)
            for trailer in single['trailers']:      # create associated buttons
                self.buttons(trailer[0], trailer[1], v_box)

    def buttons(self, text, url, box):
        """Create Button"""
        button = TrailerButton()
        button.setFixedHeight(24)
        button.setText(text)
        button.setFont(QFont('arial', 8))
        button.setToolTip(text)
        button.setStatusTip(text)
        button.setCursor(QCursor(Qt.PointingHandCursor))
        button.clicked.connect(lambda event, url=url: self.load(event, url))
        box.addWidget(button)

    def load(self, event, url):
        """Load new url to webview"""
        if self.disabled:
            self.disabled.setEnabled(True)
        self.disabled = self.sender()
        self.disabled.setEnabled(False)
        self.webview.load(QUrl(url))

    def search(self):
        """Stream videos from url"""
        dlg = UrlDialog(self)
        if dlg.exec_():
            if self.disabled:
                self.disabled.setEnabled(True)
            text = dlg.text
            url = text
            if text:
                if text.find('youtu.be') > -1:
                    code = text.split('/')[-1]
                    url = YOURL.format(code)
                elif text.find('youtube') > -1 and text.find('watch') > -1:
                    link = text.split('?')[-1]
                    code = link.split('&')[0][2:]
                    url = YOURL.format(code)
                elif text.find('youtube') > -1 and text.find('embed') > -1:
                    link = text.split('?')[0]
                    code = link.split('/')[-1]
                    url = YOURL.format(code)
                self.webview.load(QUrl(url))


class window(QMainWindow):
    """Sub-class of QMainWindow"""

    def __init__(self):
        """initialize class attributes"""
        
        super(window,self).__init__()
        self.widget = TrailerPlayer()
        self.setCentralWidget(self.widget)
        p = self.palette()
        p.setColor(QPalette.Window, Qt.black)
        self.setPalette(p)
        #self.setStyleSheet('background-color:rgba(255, 255, 255, 50)')
        self.setMinimumSize(560, 480)
        self.show()

if __name__ == '__main__':
    app=QApplication(sys.argv)
    ex=window()
    sys.exit(app.exec_())
