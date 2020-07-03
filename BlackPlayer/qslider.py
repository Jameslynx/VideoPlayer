##################################################################
# qslider.py:
# PyQt5 Custom slider, change handle to MousePressEvent position
##################################################################
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
     QSlider, QStyleOptionSlider, QStyle,
     QApplication, QFormLayout, QWidget)


class Slider(QSlider):
    """Only override the mousePressEvent method"""

    def mousePressEvent(self, event):
        """Custom mousePressEvent"""
        super(Slider, self).mousePressEvent(event)
        if event.button() == Qt.LeftButton:                 # Mouse left click
            self.val = self.pixel_post_to_range_value(event.pos())
            self.setValue(self.val)                         # Set handle to position

    def pixel_post_to_range_value(self, pos):
        """Get value of MousePress coordinates"""
        opt = QStyleOptionSlider()                          # parameters needed for drawing a slider
        self.initStyleOption(opt)                           # Set Styling parameters from opt
        gr = self.style().subControlRect(
            QStyle.CC_Slider, opt, QStyle.SC_SliderGroove, self)   # groove
        sr = self.style().subControlRect(
            QStyle.CC_Slider, opt, QStyle.SC_SliderHandle, self)   # handle

        if self.orientation() == Qt.Horizontal:
            slider_length = sr.width()              # handle width
            slider_min = gr.x()                     # groove start coor (x)
            slider_max = gr.right() - slider_length + 1  # groove max coor (x)
        else:
            slider_length = sr.height()             # handle height
            slider_min = gr.y()                     # groove start coor (y)
            slider_max = gr.bottom() - slider_length + 1  # groove max coor (y)
        pr = (pos - sr.center()) + sr.topLeft()           # New Handle center coor
        p = pr.x() if self.orientation() == Qt.Horizontal else pr.y()
        return QStyle.sliderValueFromPosition(
            self.minimum(), self.maximum(), p - slider_min,
            slider_max - slider_min, opt.upsideDown)      # return new Handle pos


class PositionSlider(Slider):
    """Sub-class for mediaPlayer Position"""

    def __init__(self, media_player, *args, **kwargs):
        super(PositionSlider, self).__init__(*args, **kwargs)
        self.media_player = media_player                        # QmediaPlayer

    def mousePressEvent(self, event):
        super(PositionSlider, self).mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self.media_player.setPosition(self.val)             # change media position


class VolumeSlider(Slider):
    """Sub-class for mediaPlayer volume"""

    def __init__(self, media_player, *args, **kwargs):
        super(VolumeSlider, self).__init__(*args, **kwargs)
        self.media_player = media_player                        # QmediaPlayer

    def mousePressEvent(self, event):
        super(VolumeSlider, self).mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self.media_player.setVolume(self.val)               # change volume

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    w = QWidget()
    flay = QFormLayout(w)
    w1 = QSlider(Qt.Horizontal)
    w2 = Slider(Qt.Horizontal)
    flay.addRow("default: ", w1)
    flay.addRow("modified: ", w2)
    w.show()
    sys.exit(app.exec_())