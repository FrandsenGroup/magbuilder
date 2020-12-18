from PyQt5 import QtWidgets
import sys
import os
import numpy as np

def popup():
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QWidget()
    w.setGeometry(50,50,300,200)

    def clicked2():
        with open('vector.npy', 'wb') as f:
            np.save(f, np.array([0]))
        w.close()

    def clicked1():
        os.chdir('./temp')
        text = line_edit.text().replace(" ", "").replace("[", "").replace("]", "").replace("(", "").replace(")", "")
        text = text.split(",")
        x = float(text[0])
        y = float(text[1])
        z = float(text[2])
        with open('vector.npy', 'wb') as f:
            np.save(f, np.array([x,y,z]))
        w.close()
    
    line_edit = QtWidgets.QLineEdit()
    line_edit.move(50,75)
    line_edit.returnPressed.connect(clicked1)

    label = QtWidgets.QLabel()
    label.setText("Vector Format:\nsx,sy,sz")
    label.move(50,50)

    b1 = QtWidgets.QPushButton()
    b1.setText("Set spin")
    b1.move(50,125)
    b1.setAutoDefault(True)
    b1.clicked.connect(clicked1)

    b2 = QtWidgets.QPushButton()
    b2.setText("Go Back")
    b2.move(50,150)
    b2.clicked.connect(clicked2)
    
    layout = QtWidgets.QVBoxLayout()
    layout.addWidget(line_edit)
    layout.addWidget(label)
    layout.addWidget(b1)
    layout.addWidget(b2)
    
    w.setLayout(layout)
    w.show()
    sys.exit(app.exec_())

popup()
