from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import sys
import os
import numpy as np

class window(QtWidgets.QWidget):
    
    def __init__(self):
        super().__init__()
        self.set_ui()

    def done(self):
        self.close()

    def keyPressEvent(self, event):
f
        if (event.key() == "enter") or (event.key() == "space"):
            self.done()

    def set_ui(self):
        self.mag = 1
        icon = QIcon('icon.png')
        self.setWindowIcon(icon)
        self.setWindowTitle('Instructions')
        self.setGeometry(50,50,300,200)

        lab = "<b>Mouse Controls</b>:<br><br><b>L. Click</b>: Select atoms for next spin assignment<br><b>R. Click</b>: Undo previous spin assignments<br><br><b>Keyboard Controls</b>:<br><br><b>Enter</b>: Assign Spins after selecting<br><b>t</b> : Toggle non-magnetic atoms<br><b>g</b> : Toggle plot grid<br><b>n</b> : Toggle ploted numbers on axes ticks<br><b>i</b> : Instructions popup<br><b>f</b>: Enter fullscreen mode<br><b>Escape</b>: Exit Program<br><b>CTRL +</b> / <b>CTRL -</b> : Zoom in or out<br><b>U / D Arrows</b>: Change atom size<br><b>R</b> / <b>L Arrows</b>: Change vector length"

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

