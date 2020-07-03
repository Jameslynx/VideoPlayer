import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import (
    QApplication, QDialog, QDialogButtonBox,
    QMainWindow, QVBoxLayout, QGridLayout,
    QLineEdit, QLabel)


class CustomDialog(QDialog):

    def __init__(self, *args, **kwargs):
        super(CustomDialog, self).__init__(*args, **kwargs)

        p = self.palette()
        p.setColor(QPalette.Window, Qt.black)   # set background color
        self.setPalette(p)

        btn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.btn_box = QDialogButtonBox(btn)
        self.btn_box.accepted.connect(self.ok)
        self.btn_box.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.init_ui()
        self.layout.addWidget(self.btn_box)
        self.setLayout(self.layout)

    def init_ui(self):
        self.setWindowTitle("Hello!")
        pass

    def ok(self):
        self.accept()

class UrlDialog(CustomDialog):

    def init_ui(self):
        self.setMaximumSize(300, 100)
        self.setMinimumSize(300, 100)
        self.setWindowTitle("Stream Video")
        self.glayout = QVBoxLayout()
        label = QLabel("URL:")
        label.setStyleSheet('color: #fefefe')
        entry = QLineEdit()
        label.setFixedWidth(30)
        self.glayout.addWidget(label, 0)
        self.glayout.addWidget(entry, 0)
        entry.editingFinished.connect(self.ok)
        self.layout.addLayout(self.glayout)
        self.entry = entry

    def ok(self):
        self.text = self.entry.text()
        self.accept()



class MainWindow(QMainWindow):


    # def __init__ etc.
    # ... not shown for clarity
        
        
    def onMyToolBarButtonClick(self, s):
        print("click", s)
        
        
        dlg = UrlDialog(self)
        if dlg.exec_():
            print("Success!")
            print(dlg.text)
        else:
            print("Cancel!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.onMyToolBarButtonClick("hi")
    main.show()
    sys.exit(app.exec_())