from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon, QPixmap
import sys
import os
import numpy as np

class window(QtWidgets.QWidget):
    
    def __init__(self):
        super().__init__()
        self.set_ui()

    def clicked2(self):
        with open('vector.npy', 'wb') as f:
            np.save(f, np.array([0]))
        self.close()

    def clicked1(self):
        os.chdir('../temp')
        text = self.line_edit.text().replace(" ", "").replace("[", "").replace("]", "").replace("(", "").replace(")", "").split(",")
        x = float(text[0])
        y = float(text[1])
        z = float(text[2])
        with open('vector.npy', 'wb') as f:
            np.save(f, np.array([x,y,z]))
        self.close()

    def check_radio(self):
        if self.b3.isChecked():
            self.label.setText("Vector Format:\na,b,c")
        else:
            self.label.setText("Vector Format:\nsx,sy,sz")

    def set_ui(self):
        icon = QIcon('iconset.png')
        self.setWindowIcon(icon)
        self.setWindowTitle('Set Spins')
        self.setGeometry(50,50,300,200)
        self.line_edit = QtWidgets.QLineEdit()
        self.line_edit.move(50,75)
        self.line_edit.returnPressed.connect(self.clicked1)

        self.label = QtWidgets.QLabel()
        self.label.setText("Vector Format:\nsx,sy,sz")
        self.label.move(50,50)

        self.b1 = QtWidgets.QPushButton()
        self.b1.setText("Set spin")
        self.b1.move(50,125)
        self.b1.setAutoDefault(True)
        self.b1.clicked.connect(self.clicked1)

        self.b2 = QtWidgets.QPushButton()
        self.b2.setText("Go Back")
        self.b2.move(50,150)
        self.b2.clicked.connect(self.clicked2)
    

        self.b3 = QtWidgets.QCheckBox("Crystallographic Coordinates")
        self.b3.toggled.connect(self.check_radio)
        self.b3.move(50,75)
            
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.line_edit)
        layout.addWidget(self.label)
        layout.addWidget(self.b1)
        layout.addWidget(self.b2)
        layout.addWidget(self.b3)
    
        self.setLayout(layout)

app = QtWidgets.QApplication(sys.argv)
win = window()
win.show()
sys.exit(app.exec_())

