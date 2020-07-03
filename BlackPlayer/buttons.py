from PyQt5 import QtCore, QtGui, QtWidgets


class Button(QtWidgets.QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMinimumSize(25, 24)

        self.color1 = QtGui.QColor('#757F9A')
        self.color2 = QtGui.QColor('#D7DDE8')

        self._animation = QtCore.QVariantAnimation(
            self,
            valueChanged=self._animate,
            startValue=0.00001,
            endValue=0.9999,
            duration=250
        )

    def _animate(self, value):
        qss = """
            color: rgb(0, 0, 0);
            border-style: solid;
            border-radius:3px;
            padding: 5px 5px 5px 5px;
        """
        grad = "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 {color1}, stop:{value} {color2}, stop: 1.0 {color1});".format(
            color1=self.color1.name(), color2=self.color2.name(), value=value
        )
        qss += grad
        self.setStyleSheet(qss)

    def enterEvent(self, event):
        self._animation.setDirection(QtCore.QAbstractAnimation.Forward)
        self._animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._animation.setDirection(QtCore.QAbstractAnimation.Backward)
        self._animation.start()
        super().enterEvent(event)

class TrailerButton(Button):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.color1 = QtGui.QColor('#e52d27')
        self.color2 = QtGui.QColor('#b31217')

        self._animation = QtCore.QVariantAnimation(
            self,
            valueChanged=self._animate,
            startValue=0.00001,
            endValue=0.9999,
            duration=250
        )      

    def _animate(self, value):

        qss = """
            height: 20px;
            color: rgb(255, 255, 255);
            border-style: solid;
            border-radius:5px;
        """
        grad = "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 {color1}, stop:{value} {color2}, stop: 1.0 {color1});".format(
            color1=self.color1.name(), color2=self.color2.name(), value=value
        )
        qss += grad
        self.setStyleSheet(qss)

class TransitionButton(Button):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.color1 = QtGui.QColor('#2B32B2')
        self.color2 = QtGui.QColor('#1488CC')

        self._animation = QtCore.QVariantAnimation(
            self,
            valueChanged=self._animate,
            startValue=0.00001,
            endValue=0.9999,
            duration=250
        )      

    def _animate(self, value):

        qss = """
            height: 20px;
            color: rgb(255, 255, 255);
            border-style: solid;
            border-radius:5px;
            padding: 5px 5px 5px 5px;
        """
        grad = "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 {color1}, stop:{value} {color2}, stop: 1.0 {color1});".format(
            color1=self.color1.name(), color2=self.color2.name(), value=value
        )
        qss += grad
        self.setStyleSheet(qss)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    w = QtWidgets.QWidget()
    lay = QtWidgets.QVBoxLayout(w)

    for i in range(5):
        button = TrailerButton()
        button.setText("Login")
        lay.addWidget(button)
    lay.addStretch()
    w.resize(640, 480)
    w.show()
    sys.exit(app.exec_())