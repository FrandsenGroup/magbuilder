from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtWidgets
import sys
import numpy as np 
from matplotlib import pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D

class ScatterClick:
    def __init__(self, pts, cif):
        self.pts = pts
        self.clicked = [0,0,0,0]
        self.fig = plt.figure()
        ax = self.fig.add_subplot(111, projection='3d')
        self.plot = ax.scatter(x,y,z,picker=True, s=55, facecolors=["C0"]*len(x), edgecolors=["C0"]*len(x))
        self.fc = self.plot.get_facecolors()
        ax.set_title(cif)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        self.numpts = 0
        ax.set_xlim3d((np.min(x) - (np.max(x)-np.min(x))/4, (np.max(x) + (np.max(x)-np.min(x))/4)))
        ax.set_ylim3d((np.min(y) - (np.max(y)-np.min(y))/4, (np.max(y) + (np.max(y)-np.min(y))/4)))
        ax.set_zlim3d((np.min(z) - (np.max(z)-np.min(z))/4, (np.max(z) + (np.max(z)-np.min(z))/4)))

        self.fig.canvas.mpl_connect('close_event',self.on_close)
        self.fig.canvas.mpl_connect('pick_event',self.on_press)
        plt.show()

    def on_close(self, event):
        with open('cords.npy', 'wb') as f:
            np.save(f, self.clicked)
        plt.close()

    def on_press(self, event):
        ind = event.ind
        self.numpts += 1
        if len(self.clicked) == 4:
            self.clicked = np.array([x[ind], y[ind], z[ind]])
        else:
            self.clicked = np.concatenate([self.clicked.reshape(self.numpts-1, 3), np.array([x[ind], y[ind], z[ind]]).reshape(1,3)], axis=0)
        for i in list(ind): # might be more than one point if ambiguous click
            self.fc[i,:] = (1, 0, 0, 1)
            self.plot._facecolor3d = self.fc
            self.plot._edgecolor3d = self.fc
        self.fig.canvas.draw_idle()

with open('points.npy', 'rb') as f:
    x = np.load(f)
    y = np.load(f)
    z = np.load(f)
    cif = np.load(f)
pts = np.array([x,y,z]).T
ScatterClick(pts, cif)

