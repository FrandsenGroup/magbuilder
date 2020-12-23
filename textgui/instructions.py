from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon, QPixmap
import sys
import os
import numpy as np

class window(QtWidgets.QWidget):
    
    def __init__(self):
        super().__init__()
        self.set_ui()

    def done(self):
        self.close()

    def set_ui(self):
        self.mag = 1
        icon = QIcon('icon.png')
        self.setWindowIcon(icon)
        self.setWindowTitle('Instructions')
        self.setGeometry(50,50,300,200)

        lab = "Mouse:\nL. Click: Select atoms for next spin assignment\nR. Click: Undo previous spin assignments\n\nKeyboard:\nEnter: Assign Spins after selecting\nt : Toggle non-magnetic atoms\ni : Instructions popup\nEscape: Exit Program\nCTRL + / CTRL - : Zoom in or out\nU / D Arrows: Change atom size\nR / L Arrows: Change vector length"

        self.l1 = QtWidgets.QLabel()
        self.l1.setText(lab)
        self.l1.move(50,0)

        self.b1 = QtWidgets.QPushButton()
        self.b1.setText("Done")
        self.b1.move(50,25)
        self.b1.setAutoDefault(True)
        self.b1.clicked.connect(self.done)
                    
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.l1)
        layout.addWidget(self.b1)
        self.setLayout(layout)

app = QtWidgets.QApplication(sys.argv)
win = window()
win.show()
sys.exit(app.exec_())

