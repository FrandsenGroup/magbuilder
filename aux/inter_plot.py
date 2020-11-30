from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtWidgets
import sys
import os
import numpy as np 
from matplotlib import pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D

class ScatterClick:
    def __init__(self, pts, cif, cords_list, vector_list):
        self.pts = pts
        self.get_usable_pts(cords_list)

        # initialize 3d plot and save attributes    
        self.clicked = []
        self.fig = plt.figure()
        ax = self.fig.add_subplot(111, projection='3d')
        # changeable plot
        self.plot = ax.scatter(self.usable[:,0],self.usable[:,1],self.usable[:,2],
                               picker=True, s=55, facecolors=["C0"]*len(self.usable[:,0]),
                               edgecolors=["C0"]*len(self.usable[:,0]))
        # scatterplot that wont interact or change color
        if len(self.fixed) != 0:
            ax.scatter(self.fixed[:,0],self.fixed[:,1],self.fixed[:,2], s=55, 
                       facecolors='red', edgecolors='red', label="Magnetic")
        # graph settings
        self.fc = self.plot.get_facecolors()
        self.ogcolor = self.fc[0,:].copy()
        ax.set_title(cif)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")

        self.numpts = 0
        x, y, z = pts[:,0], pts[:,1], pts[:,2]
        ax.set_xlim3d((np.min(x) - (np.max(x)-np.min(x))/4, (np.max(x) + (np.max(x)-np.min(x))/4)))
        ax.set_ylim3d((np.min(y) - (np.max(y)-np.min(y))/4, (np.max(y) + (np.max(y)-np.min(y))/4)))
        ax.set_zlim3d((np.min(z) - (np.max(z)-np.min(z))/4, (np.max(z) + (np.max(z)-np.min(z))/4)))
        self.x, self.y, self.z = self.usable[:,0], self.usable[:,1], self.usable[:,2]

        # plot arrows if called for
        for i in range(len(vector_list)):
            plt.quiver(cords_list[i][:,0], cords_list[i][:,1], 
                        cords_list[i][:,2], vector_list[i][0], 
                        vector_list[i][1], vector_list[i][2], 
                        length=(np.max(x) - np.min(x))/1.5, color="black")
        # initialize functions called upon events
        self.fig.canvas.mpl_connect('close_event',self.on_close)
        self.fig.canvas.mpl_connect('pick_event',self.on_press)
        self.fig.canvas.mpl_connect('key_release_event',self.on_close)
        plt.show()

    def get_usable_pts(self, cords_list):
        if len(cords_list) > 0:
            used_cords = np.concatenate(cords_list, axis=0) 
            assigned = list(zip(used_cords[:,0],used_cords[:,1],used_cords[:,2]))
            usable = []
            fixed = []
            for i in self.pts:
                if (i[0], i[1], i[2]) not in assigned:
                    usable += [i]
                else:
                    fixed += [i]
            self.usable = np.array(usable)
            self.fixed = np.array(fixed)
        else:
            self.usable = self.pts.copy()
            self.fixed = np.array([])

    def on_close(self, event):
        # closing the program saves clicked positions to external file
        with open('cords.npy', 'wb') as f:
            np.save(f, self.clicked)
        plt.close()

    def on_press(self, event):
        # clicking the artist changes the color and saves the coords in self.clicked
        #
        ind = event.ind
        self.numpts += 1
        # build array of points clicked
        if len(self.clicked) == 0:
            self.clicked = np.array([self.x[ind], self.y[ind], self.z[ind]]).reshape(1,3)
        else:
            self.clicked = np.concatenate([self.clicked.reshape(self.numpts-1, 3),
                           np.array([self.x[ind], self.y[ind], self.z[ind]]).reshape(1,3)],
                           axis=0)
        for i in list(ind): # might be more than one point if ambiguous click
            # find if the clicked point is already in the clicked attribute
            if not np.allclose(self.fc[i,:], np.array([1, 0, 0, 1])):
                self.fc[i,:] = (1, 0, 0, 1)
                self.plot._facecolor3d = self.fc
                self.plot._edgecolor3d = self.fc
            else:
                # if this is the case, remove both clicks from the matrix 
                # and reset the color / numpts
                dup = self.clicked[-1,:].ravel()
                self.clicked = self.clicked[:-1, :].copy()
                m , n = self.clicked.shape
                if m == 1:
                    self.clicked = []
                else:
                    new = []
                    for j in range(m):
                        if not np.allclose(dup, self.clicked[j]):
                            new += [self.clicked[j]]
                    self.clicked = np.array(new)
                self.fc[i,:] = self.ogcolor
                self.plot._facecolor3d = self.fc
                self.plot._edgecolor3d = self.fc
                self.numpts = self.numpts - 2 
        self.fig.canvas.draw_idle()

# navigate to and open structure data
os.chdir('../temp')
with open('points.npy', 'rb') as f:
    x = np.load(f)
    y = np.load(f)
    z = np.load(f)
    cif = np.load(f)
# check for previous iteration vectors to plot
with open('arrows.npy', 'rb') as f:
    cords_list = np.load(f, allow_pickle=True)
    vector_list = np.load(f, allow_pickle=True)
pts = np.array([x,y,z]).T
#plot and interact via ScatterClick class
ScatterClick(pts, cif, cords_list, vector_list)

