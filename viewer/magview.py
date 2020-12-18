import numpy as np 
import matplotlib as mpl
from matplotlib import pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
import os
import numpy.linalg as la

class MagView:
    def __init__(self, X, cif, l, s):
        """
        X : n x 7 ndarray with coordinate points in first 3 cols, 
                      1 for if theres a vector in col 4 and  has
                      the associated vectors in 5,6,7
        cif : filename
        l = size for arrows
        s = dot size
        """
        self.clicked = []                      # to contain points receiving a vector
        self.l = l                             # default length of arrows
        self.s = s                             # default size of point
        self.X = X                             # X matrix containing coordinates and vectors
        self.fig = plt.figure(figsize=(8.,6.)) # set and save figure object
        self.ax = self.fig.add_subplot(111, projection='3d') # make 3d
        self.plotted = []
        
        #scatter the structure data
        self.plot = self.ax.scatter(self.X[:,0],self.X[:,1],self.X[:,2],
                               picker=True, s=self.s, facecolors=["C0"]*len(self.X[:,0]),
                               edgecolors=["C0"]*len(self.X[:,0]))
        
        self.set_plot_params(cif) # set color, axes, labels, title
        self.set_text()
        

        # plot quiver of arrows
        self.quiver = self.ax.quiver(self.X[:,0], self.X[:,1], self.X[:,2],
                        self.X[:,4], self.X[:,5], self.X[:,6], 
                        length=2*self.scaling_magnitude/self.l,
                        color="black", pivot="middle", arrow_length_ratio=0.3)

        # initialize functions called upon events
        self.fig.canvas.mpl_connect('close_event',self.on_close) # D, escape, enter
        self.fig.canvas.mpl_connect('pick_event',self.on_click) # click on plotted point
        self.fig.canvas.mpl_connect('key_release_event',self.on_key_press) # zoom / scale 
        plt.show()

    def set_text(self):
        # text instructions on plot GUI
        self.ax.text2D(0.22,-0.04, 
        "Enter:", transform=self.ax.transAxes, fontweight='bold')
        self.ax.text2D(0.31,-0.04, 
        "Assign spins", transform=self.ax.transAxes)
        self.ax.text2D(0.46,-0.04, 
        "Escape:", transform=self.ax.transAxes, fontweight='bold')
        self.ax.text2D(0.56,-0.04, 
        "Exit Program", transform=self.ax.transAxes)
        self.ax.text2D(-.05,-0.08, 
        "Right Click:", transform=self.ax.transAxes, fontweight='bold')
        self.ax.text2D(0.11,-0.08, 
        "Select next spin assignments or deselect", transform=self.ax.transAxes)
        self.ax.text2D(-0.15,-0.12, 
        "Left Click:", transform=self.ax.transAxes, fontweight='bold')
        self.ax.text2D(-0.01,-0.12, 
        "Undo previous spin assignment ", transform=self.ax.transAxes)
        self.ax.text2D(0.350,-0.12, 
        "U / D Arrows:", transform=self.ax.transAxes, fontweight='bold')
        self.ax.text2D(0.525,-0.12, 
        "Change atom size", transform=self.ax.transAxes)
        self.ax.text2D(0.740,-0.12, 
        "R / L Arrows:", transform=self.ax.transAxes, fontweight='bold')
        self.ax.text2D(0.91,-0.12, 
        "Change arrow size", transform=self.ax.transAxes)
        self.ax.text2D(.58,-0.08, 
        "CTRL + / CTRL -:", transform=self.ax.transAxes, fontweight='bold')
        self.ax.text2D(.79,-0.08, 
        "Zoom in or out", transform=self.ax.transAxes)
             
    def set_plot_params(self, cif):
        # set colors
        self.blue = np.array([0.12156863, 0.4666667, 0.70588235, 1.])
        self.red = np.array([1,0,0,1])
        self.fc = self.plot.get_facecolors()

        # graph cosmetics
        title = "\n\n"+str(cif)
        self.fig.suptitle(title, fontweight='bold')
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_zticks([])
        self.ax.set_xlabel("X", fontweight='bold')
        self.ax.set_ylabel("Y", fontweight='bold')
        self.ax.set_zlabel("Z", fontweight='bold')
            
        # center and scale all axes equally
        self.centroid = np.sum(self.X[:,:3], axis=0) / len(self.X)
        self.scaling_magnitude = np.max(np.abs(self.X[:,:3] - self.centroid))
        self.zoom = 1.2
        self.axes_lim()
            
    def axes_lim(self):
        #scale and center plot
        self.ax.set_xlim3d(self.centroid[0] - self.zoom*self.scaling_magnitude, self.centroid[0] + self.zoom*self.scaling_magnitude)
        self.ax.set_ylim3d(self.centroid[1] - self.zoom*self.scaling_magnitude, self.centroid[1] + self.zoom*self.scaling_magnitude)
        self.ax.set_zlim3d(self.centroid[2] - self.zoom*self.scaling_magnitude, self.centroid[2] + self.zoom*self.scaling_magnitude)
    
    def on_close(self, event):
        with open('X.npy', 'wb') as f:
            np.save(f, self.X)
        
    def enter(self):
        if (len(self.clicked) != 0):
            self.fig.canvas.draw_idle()
            os.chdir('..')
            os.system('python3 window.py') 
            os.chdir('./temp')
            with open('vector.npy', 'rb') as f:
                vector = np.load(f)
            
            if len(vector) != 1:
                norm = la.norm(vector)
                if norm != 0:
                    self.X[np.array(self.clicked),4:] = vector / norm
                    self.X[np.array(self.clicked),3] = 1
            self.clicked = []
            self.redraw_arrows()
            self.fig.canvas.draw_idle()
            self.plotted = (self.X[:,3] == 1).nonzero()                 

    def on_key_press(self, event):

        if event.key == "enter": # proceed to save and continue to vector assignemnt
            self.enter()
        elif (event.key == "escape"): # end program
            plt.close()

        else:
            if (event.key == "right") and (len(self.plotted) != 0): # grow arrow
                self.l = 0.9*self.l
                self.redraw_arrows()
            elif (event.key == "left") and (len(self.plotted) != 0): # shrink arrow
                self.l = 10*self.l/9
                self.redraw_arrows()
            elif event.key == "down": # shrink size of point
                self.s = 0.9*self.s
                self.redraw_scatter()
            elif event.key == "up": # grow size of point
                self.s = 10*self.s/9
                self.redraw_scatter()
            elif event.key == "ctrl+-": # zoom into structure
                self.zoom = 10*self.zoom/9
                self.axes_lim()
            elif event.key == "ctrl+=": # zoom out of structure
                self.zoom = 9*self.zoom/10 
                self.axes_lim()
        if event.key in ["right","left","down","up","ctrl+-","ctrl+="]:
            # update canvas
            self.fig.canvas.draw_idle()

    def redraw_arrows(self):
        #remove and replot arrows
        self.quiver.remove()
        self.quiver = self.ax.quiver(self.X[:,0], self.X[:,1], self.X[:,2], self.X[:,4], 
                                     self.X[:,5], self.X[:,6], 
                                     length=2*self.scaling_magnitude/self.l, 
                                     color="black", pivot="middle", arrow_length_ratio=0.3)
    def redraw_scatter(self):
        # remove and replot scattered points
        self.plot.remove()
        self.plot = self.ax.scatter(self.X[:,0],self.X[:,1],self.X[:,2],
                               picker=True, s=self.s, facecolors=self.fc,
                               edgecolors=self.fc)

    def on_click(self, event):
        # clicking the artist changes the color and saves the coords in self.clicked

        ind = event.ind
        point = np.array([self.X[ind,0], self.X[ind,1], self.X[ind,2]])
        fixed = True if np.sum(self.X[ind,3]) > 0 else False

        if str(event.mouseevent.button) == "MouseButton.LEFT" and not fixed:
            for i in ind:
                if i not in self.clicked:
                    self.clicked += [i]
                    self.fc[i,:] = self.red
                else:
                    self.clicked.remove(i)
                    self.fc[i,:] = self.blue
                self.plot._facecolor3d = self.fc
                self.plot._edgecolor3d = self.fc
            
        elif str(event.mouseevent.button) == "MouseButton.RIGHT" and fixed:
           
            self.X[np.array(ind),3:] = np.zeros(4)
            self.redraw_arrows()   
            self.fc[np.array(ind),:] = self.blue
            for i in ind:
                if i in self.clicked:
                     self.clicked.remove(i)
            self.plot._facecolor3d = self.fc
            self.plot._edgecolor3d = self.fc
            self.plotted = (self.X[:,3] == 1).nonzero() 
        self.fig.canvas.draw_idle()

mpl.rcParams['toolbar'] = 'None'       # remove matplotlib toolbar