import os
import numpy as np 
import matplotlib as mpl
from matplotlib import pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D


class ScatterClick:
    def __init__(self, X, cif, l, s):
        """
        X : n x 7 ndarray with coordinate points in first 3 cols, 
                      1 for if theres a vector in col 4 and  has
                      the associated vectors in 5,6,7
        cif : filename
        l = size for arrows
        s = dot size
        """
        self.undone = []                       # to contain removed vectors if any
        self.clicked = []                      # to contain points receiving a vector
        self.l = l                             # default length of arrows
        self.s = s                             # default size of point
        self.X = X                             # X matrix containing coordinates and vectors
        self.fig = plt.figure(figsize=(8.,6.)) # set and save figure object
        mpl.rcParams['toolbar'] = 'None'       # remove matplotlib toolbar
        self.ax = self.fig.add_subplot(111, projection='3d') # make 3d
        plotted, _ = (X == 1).nonzero()        
        self.plotted = list(set(plotted))      # indexes with associated vectors

        #scatter the structure data
        self.plot = self.ax.scatter(self.X[:,0],self.X[:,1],self.X[:,2],
                               picker=True, s=self.s, facecolors=["C0"]*len(self.X[:,0]),
                               edgecolors=["C0"]*len(self.X[:,0]))
        
        self.set_plot_params(cif) # set color, axes, labels, title

        # plot quiver of arrows
        self.quiver = self.ax.quiver(self.X[:,0], self.X[:,1], self.X[:,2],
                        self.X[:,4], self.X[:,5], self.X[:,6], 
                        length=2*self.scaling_magnitude/self.l,
                        color="black", pivot="middle", arrow_length_ratio=0.3)

        # initialize functions called upon events
        self.fig.canvas.mpl_connect('close_event',self.on_close) # D, escape, enter
        self.fig.canvas.mpl_connect('pick_event',self.on_press) # click on plotted point
        self.fig.canvas.mpl_connect('key_release_event',self.on_enter) # zoom / scale 
        plt.show()
        
    def set_plot_params(self, cif):
            # set colors
            self.blue = np.array([0.12156863, 0.4666667, 0.70588235, 1.])
            self.red = np.array([1,0,0,1])
            self.fc = self.plot.get_facecolors()
            # set plotted colors to red
            if len(self.plotted) != 0:
                self.fc[np.array(self.plotted),:] = self.red
                self.plot._facecolor3d = self.fc
                self.plot._edgecolor3d = self.fc

            # graph cosmetics
            self.ax.set_title(cif)
            self.ax.set_xticks([])
            self.ax.set_yticks([])
            self.ax.set_zticks([])
            self.ax.set_xlabel("X")
            self.ax.set_ylabel("Y")
            self.ax.set_zlabel("Z")
            
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
        # closing the program saves clicked positions to external file
        # when there was something done

        if (len(self.clicked) > 0) or (len(self.undone) > 0):
            with open('cords.npy', 'wb') as f: # save data and assign vector
                np.save(f, self.clicked)
                np.save(f, self.undone)
                np.save(f, self.l)
                np.save(f, self.s)
            if (len(self.clicked) == 0): # pass to skip vector assignment
                with open('vector.npy', 'wb') as f:
                    np.save(f, [0])

        # if nothing was done
        elif (len(self.clicked) == 0) and (len(self.undone) == 0):
            self.kill()
    
    def on_enter(self, event):

        if event.key == "enter": # proceed to save and continue to vector assignemnt
            plt.close()
        elif (event.key == "d" or event.key == "escape"): # end program
            self.kill()
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
               
    def kill(self):
        # end program and save altered data
        with open('done.npy', 'wb') as f:
            np.save(f, True) 

               

    def on_press(self, event):
        # clicking the artist changes the color and saves the coords in self.clicked
        #

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
            for i in ind:
                if self.X[i,3] != 0:
                    self.undone += [i]
                self.X[i,3:] = np.zeros(4)
            self.redraw_arrows()   
            self.fc[i,:] = self.blue
            self.plot._facecolor3d = self.fc
            self.plot._edgecolor3d = self.fc
        self.fig.canvas.draw_idle()

          
mpl.rcParams['toolbar'] = 'None'
# navigate to and open structure and vector data
os.chdir('../temp')
with open('points.npy', 'rb') as f:
    X = np.load(f)
    k = np.load(f)
    s = np.load(f)
    cif = np.load(f)

#plot and interact via ScatterClick class
ScatterClick(X, cif, k, s)


