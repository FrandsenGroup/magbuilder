from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
import sys
import os
import numpy as np
import re

# prop vector regex
#  r"^(\({1}((\d+\.{1}\d+|\d+|.\d+),){2}(\d+\.{1}\d+|\d+|.\d+)\){1},)*(\({1}((\d+\.{1}\d+|\d+|.\d+),){2}(\d+\.{1}\d+|\d+|.\d+)\){1})$"
#

class window(QtWidgets.QWidget):
    """
    Popup window that prompts the user to input the 
        spin, magnitude, and propagation vector
    """
    def __init__(self):
        super().__init__()
        self.set_ui()

    def close_no_save(self):
        #
        with open('vector.npy', 'wb') as f:
            np.save(f, np.array([0]))
        self.close()

    def save_data(self):

        self.reset_labels()

        ### try to read vector and correct format
        text = self.line_vec.text().replace("]", ")").replace("[", "(").replace("{", "(").replace("}", ")").replace(" ", "").replace("\t", "").replace("\n", "")

        try:
            text = text.replace("(","").replace(")","").split(",")
            [x, y, z] = list(map(float, text))

        except ValueError:

            if self.b3.isChecked():
                self.veclabel.setText("<b>Magnetic Moment Vector</b><br>Format: <b>a,b,c</b><br><b>Entry did not match the format.  Try again.</b>")

            else:
                self.veclabel.setText("<b>Magnetic Moment Vector</b><br>Format: <b>sx,sy,sz</b><br><b>Entry did not match the format.  Try again.</b>")
            return

        ### 
        
        prop = self.line_prop.text().replace("]", ")").replace("[", "(").replace("{", "(").replace("}", ")").replace(" ", "").replace("\t", "").replace("\n", "")
        if prop == "":
            prop_vec = [[0,0,0]]

        elif "),(" in prop:
            prop = prop.replace("),(",");(")
            d = prop.split(";")
            prop_vec = []
            try:
                for i in range(len(d)):
                    l = d[i].replace("(", "").replace(")", "").split(",")
                    [p1, p2, p3] = list(map(float, l))
                    prop_vec += [[p1, p2, p3]]
            except ValueError:
                self.proplabel.setText("<b>Propagation Vector</b><br>Format: <b>k1,k2,k3</b><br>(Optional: will default to (0, 0, 0))<br>Entry did not match format for either single<br>or multiple propagation vectors.<br><b>Try again</b>")
                return

        else:
            prop = prop.replace("(","").replace(")","").split(",")
            try:
                [p1, p2, p3] = list(map(float, prop))                
                prop_vec = [[p1,p2,p3]]
            except ValueError:
                self.proplabel.setText("<b>Propagation Vector</b><br>Format: <b>k1,k2,k3</b><br>(Optional: will default to (0, 0, 0))<br>Entry did not match format for either single<br>or multiple propagation vectors.<br><b>Try again</b>")
                return

        ### check magnitude 
        if self.line_mag.text() != "":
            try:
                mag = float(eval(self.line_mag.text()))

            except ValueError:
                self.maglabel.setText("<b>Display Magnitude</b><br>(Optional: will default to length of magnetic moment)<br><b>Magnitude must be integer or decimal!</b>")
                return

        else:

            mag = np.sqrt(x**2 + y**2 + z**2)
        
        os.chdir('../output')
        with open('vector.npy', 'wb') as f:
            np.save(f, np.array([x,y,z]))
            np.save(f, mag)
            np.save(f, self.b3.isChecked())
            np.save(f, prop_vec)
        self.close()

    def reset_labels(self):
        self.maglabel.setText("<b>Display Magnitude</b><br>(Optional: will default to length of magnetic moment)")
        self.veclabel.setText("<b>Spin Vector</b><br>Format: <b>sx,sy,sz</b>")
        self.proplabel.setText("<b>Propagation Vector</b><br>Format: <b>k1,k2,k3</b><br>(Optional: will default to (0, 0, 0))")

    def check_radio(self):
        if self.b3.isChecked():
            self.veclabel.setText("<b>Magnetic Moment Vector</b><br>Format: <b>a,b,c</b>")
        else:
            self.veclabel.setText("<b>Magnetic Moment Vector</b><br>Format: <b>sx,sy,sz</b>")

    def set_ui(self):

        self.multiple_props = re.compile(r"^(\({1}((\d+\.{1}\d+|\d+\/{1}\d+|\d+|.\d+),){2}(\d+\.{1}\d+|\d+\/{1}\d+|\d+|.\d+)\){1},)*(\({1}((\d+\.{1}\d+|\d+\/{1}\d+|\d+|.\d+),){2}(\d+\.{1}\d+|\d+\/{1}\d+|\d+|.\d+)\){1})$")
        self.single_prop = re.compile(r"^((\d+\.{1}\d+|\d+\/{1}\d+|\d+|.\d+),){2}(\d+\.{1}\d+|\d+\/{1}\d+|\d+|.\d+)$")
        
        self.mag = 1
        icon = QIcon('iconset.png')
        self.setWindowIcon(icon)
        self.setWindowTitle('Set Spins')
        self.setGeometry(50,50,300,200)
        self.line_vec = QtWidgets.QLineEdit()
        self.line_vec.move(50,25)
        self.line_vec.returnPressed.connect(self.save_data)

        self.veclabel = QtWidgets.QLabel()
        self.veclabel.move(50,0)
        
        self.maglabel = QtWidgets.QLabel()
        self.maglabel.move(50,75)
        
        self.line_mag = QtWidgets.QLineEdit()
        self.line_mag.move(50,25)
        self.line_mag.returnPressed.connect(self.save_data)

        self.proplabel = QtWidgets.QLabel()
        self.proplabel.move(50,85)

        self.line_prop = QtWidgets.QLineEdit()
        self.line_prop.move(50,25)
        self.line_prop.returnPressed.connect(self.save_data)

        self.multlabel = QtWidgets.QLabel()
        self.multlabel.setText("<i>For Multiple Propagation Vectors:<br>insert in tuples of 3, delimited by commas:<br>Ex: (0,0.5,0.5), (1,0,0.5), ...</i>")
        self.multlabel.move(50,95)

        self.b1 = QtWidgets.QPushButton()
        self.b1.setText("Set spin")
        self.b1.move(50,100)
        self.b1.setAutoDefault(True)
        self.b1.clicked.connect(self.save_data)

        self.b2 = QtWidgets.QPushButton()
        self.b2.setText("Go Back")
        self.b2.move(100,100)
        self.b2.clicked.connect(self.close_no_save)    

        self.b3 = QtWidgets.QCheckBox("Crystallographic Coordinates (a, b, c)")
        self.b3.toggled.connect(self.check_radio)
        self.b3.move(50,50)

        self.reset_labels()
        
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.veclabel)
        layout.addWidget(self.line_vec)
        layout.addWidget(self.b3)
        layout.addWidget(self.maglabel)
        layout.addWidget(self.line_mag)
        layout.addWidget(self.proplabel)
        layout.addWidget(self.line_prop)
        layout.addWidget(self.multlabel)  
        layout.addWidget(self.b1)
        layout.addWidget(self.b2)
        
        self.setLayout(layout)

app = QtWidgets.QApplication(sys.argv)
win = window()
win.show()
sys.exit(app.exec_())

