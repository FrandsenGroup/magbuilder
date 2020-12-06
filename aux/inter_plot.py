from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtWidgets
import sys
import os
import numpy as np 
from matplotlib import pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
import matplotlib as mpl

class ScatterClick:
    def __init__(self, pts, cif, plotted, vectors, k):
        self.pts = pts
        
        X = np.zeros((len(pts), 7))
        X[:,:3] = pts
        if len(plotted) > 0:
            X[np.array(plotted).ravel(),3] = 1
            X[:,4:] = vectors
        self.k = k
        self.X = X
        mpl.rcParams['toolbar'] = 'None'
        # initialize 3d plot and save attributes    
        self.clicked = []
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        # changeable plot
        
        self.plot = self.ax.scatter(self.X[:,0],self.X[:,1],self.X[:,2],
                               picker=True, s=55, facecolors=["C0"]*len(self.X[:,0]),
                               edgecolors=["C0"]*len(self.X[:,0]))
        
        self.fc = self.plot.get_facecolors()
        self.ogcolor = self.fc[0,:].copy()
        if len(plotted) != 0:
            self.fc[np.array(plotted),:] = np.array([1, 0, 0, 1])
            self.plot._facecolor3d = self.fc
            self.plot._edgecolor3d = self.fc
        # graph settings
        self.plotted = plotted
        self.ax.set_title(cif)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_zticks([])
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set_zlabel("Z")

        self.ax.set_xlim3d((np.min(self.X[:,0]) - (np.max(self.X[:,0])-np.min(self.X[:,0]))/4, (np.max(self.X[:,0]) + (np.max(self.X[:,0])-np.min(self.X[:,0]))/4)))
        self.ax.set_ylim3d((np.min(self.X[:,1]) - (np.max(self.X[:,1])-np.min(self.X[:,1]))/4, (np.max(self.X[:,1]) + (np.max(self.X[:,1])-np.min(self.X[:,1]))/4)))
        self.ax.set_zlim3d((np.min(self.X[:,2]) - (np.max(self.X[:,2])-np.min(self.X[:,2]))/4, (np.max(self.X[:,2]) + (np.max(self.X[:,2])-np.min(self.X[:,2]))/4)))
        
        # plot arrows if called for

        self.quiver = self.ax.quiver(self.X[:,0], self.X[:,1], self.X[:,2],
                                self.X[:,4], self.X[:,5], self.X[:,6], 
                                length=(np.max(self.X[:,0]) - np.min(self.X[:,0]))/self.k,
                                color="black", 
                                pivot="middle")

        # initialize functions called upon events
        self.fig.canvas.mpl_connect('close_event',self.on_close)
        self.fig.canvas.mpl_connect('pick_event',self.on_press)
        self.fig.canvas.mpl_connect('key_press_event',self.on_enter)
        plt.show()

    def on_close(self, event):
        # closing the program saves clicked positions to external file
        if len(self.clicked) > 0:
            with open('cords.npy', 'wb') as f:
                np.save(f, self.clicked)
                np.save(f, self.k)
            plt.close()
        else:
            self.kill()
    
    def on_enter(self, event):
        if event.key == "enter":
            self.on_close("enter")
        elif (event.key == "d" or event.key == "escape"):
            self.kill()
        elif event.key == "l":
            self.k *= 0.9
            self.redraw_arrows()
        elif event.key == "s":
            self.k *= 10/9
            self.redraw_arrows()
        
        self.fig.canvas.draw_idle()

    def redraw_arrows(self):
        self.quiver.remove()
        self.quiver = self.ax.quiver(self.X[:,0], self.X[:,1], self.X[:,2], self.X[:,4], 
                                     self.X[:,5], self.X[:,6], 
                                     length=(np.max(x) - np.min(x))/self.k, color="black",
                                     pivot="middle")
        for line in self.ax.xaxis.get_ticklines():
            line.set_visible(False)
        for line in self.ax.yaxis.get_ticklines():
            line.set_visible(False)
        for line in self.ax.zaxis.get_ticklines():
            line.set_visible(False)
               
    def kill(self):
        with open('done.npy', 'wb') as f:
            np.save(f, True) 
        plt.close()
               

    def on_press(self, event):
        # clicking the artist changes the color and saves the coords in self.clicked
        #

        ind = event.ind
        point = np.array([self.X[ind,0], self.X[ind,1], self.X[ind,2]])
        fixed = False

        for i in ind:
            if self.X[i,3] == 1:
                fixed = True
                break

        if str(event.mouseevent.button) == "MouseButton.LEFT" and not fixed:
            for i in ind:
                if i not in self.clicked:
                    self.clicked += [i]
                    self.fc[i,:] = (1, 0, 0, 1)
                    
                else:
                    self.clicked.remove(i)
                    self.fc[i,:] = self.ogcolor
                    
                self.plot._facecolor3d = self.fc
                self.plot._edgecolor3d = self.fc
            
        elif str(event.mouseevent.button) == "MouseButton.RIGHT" and fixed:
            for i in ind:
                self.X[i,3:] = np.zeros(4)
            self.quiver.remove()
            self.quiver = self.ax.quiver(self.X[:,0], self.X[:,1], self.X[:,2], self.X[:,4], 
                                         self.X[:,5], self.X[:,6], 
                                         length=(np.max(x) - np.min(x))/self.k, color="black",
                                         pivot="middle")    
            self.fc[i,:] = self.ogcolor
            self.plot._facecolor3d = self.fc
            self.plot._edgecolor3d = self.fc
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
    cords = np.load(f, allow_pickle=True)
    arrows = np.load(f, allow_pickle=True)
    k = np.load(f, allow_pickle=True)
pts = np.array([x,y,z]).T
#plot and interact via ScatterClick class
ScatterClick(pts, cif, cords, arrows, k)

