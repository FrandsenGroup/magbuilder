from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
import sys
import os
import numpy as np

class window(QtWidgets.QWidget):
    """
    Popup window that sets prompts the user to input the 
        spin, magnitude, and propagation vector
    """
    def __init__(self):
        super().__init__()
        self.set_ui()

    def clicked2(self):
        #
        with open('vector.npy', 'wb') as f:
            np.save(f, np.array([0]))
        self.close()

    def clicked1(self):
        if self.line_edit2.text() != "":
            try:
                self.mag = float(self.line_edit2.text())
            except:
                self.maglabel.setText("<b>Magnitude</b><br>(Optional: will default to unit length)<br><b>Magnitude must be integer or decimal!</b>")
                return
        try:
            text = self.line_edit1.text().replace(" ", "").replace("[", "")
            text = text.replace("]", "").replace("(", "").replace(")", "").split(",")
            x = float(text[0])
            y = float(text[1])
            z = float(text[2])
        except:
            self.label.setText("<b>Spin Vector</b><br>Format: <b>sx,sy,sz</b><br><b>Entry did not match the format.  Try again.</b>")
            return
        os.chdir('../temp')
        with open('vector.npy', 'wb') as f:
            np.save(f, np.array([x,y,z]))
            np.save(f, self.mag)
        self.close()
        
        print("Enter Vector in the format \"1,2,3\" and magnitude as a int/float")

        

    def check_radio(self):
        if self.b3.isChecked():
            self.label.setText("<b>Spin Vector</b><br>Format: <b>a,b,c</b>")
        else:
            self.label.setText("<b>Spin Vector</b><br>Format: <b>sx,sy,sz</b>")

    def set_ui(self):
        self.mag = 1
        icon = QIcon('iconset.png')
        self.setWindowIcon(icon)
        self.setWindowTitle('Set Spins')
        self.setGeometry(50,50,300,200)
        self.line_edit1 = QtWidgets.QLineEdit()
        self.line_edit1.move(50,25)
        self.line_edit1.returnPressed.connect(self.clicked1)

        self.label = QtWidgets.QLabel()
        self.label.setText("<b>Spin Vector</b><br>Format: <b>sx,sy,sz</b>")
        self.label.move(50,0)
        
        self.maglabel = QtWidgets.QLabel()
        self.maglabel.setText("<b>Magnitude</b><br>(Optional: will default to unit length)")
        self.maglabel.move(50,75)

        self.line_edit2 = QtWidgets.QLineEdit()
        self.line_edit2.move(50,25)
        self.line_edit2.returnPressed.connect(self.clicked1)

        self.proplabel = QtWidgets.QLabel()
        self.proplabel.setText("<b>Propagation Vector</b><br>(Optional: will default to [0, 0, 0])")
        self.proplabel.move(50,85)

        self.line_edit3 = QtWidgets.QLineEdit()
        self.line_edit3.move(50,25)
        self.line_edit3.returnPressed.connect(self.clicked1)

        self.b1 = QtWidgets.QPushButton()
        self.b1.setText("Set spin")
        self.b1.move(50,100)
        self.b1.setAutoDefault(True)
        self.b1.clicked.connect(self.clicked1)

        self.b2 = QtWidgets.QPushButton()
        self.b2.setText("Go Back")
        self.b2.move(100,100)
        self.b2.clicked.connect(self.clicked2)
    

        self.b3 = QtWidgets.QCheckBox("Crystallographic Coordinates (a, b, c)")
        self.b3.toggled.connect(self.check_radio)
        self.b3.move(50,50)
            
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.line_edit1)
        layout.addWidget(self.b3)
        layout.addWidget(self.maglabel)
        layout.addWidget(self.line_edit2)
        layout.addWidget(self.proplabel)
        layout.addWidget(self.line_edit3)
        layout.addWidget(self.b1)
        layout.addWidget(self.b2)   

        self.setLayout(layout)

app = QtWidgets.QApplication(sys.argv)
win = window()
win.show()
sys.exit(app.exec_())

