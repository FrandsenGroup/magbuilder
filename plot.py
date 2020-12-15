#
#
#
#
# imports
import os
from tkinter import filedialog
import tkinter as tk
import numpy.linalg as la
import numpy as np 
from matplotlib import pyplot as plt
from diffpy.structure import loadStructure
from mpl_toolkits.mplot3d import Axes3D

def update(X, vector, cords, undone):
    #erase undone vectors
    if len(undone) != 0:
            X[undone, 3:] = 0
    # add new vector
    if len(vector) != 1 and len(cords):
        vector = vector / la.norm(vector)
        X[cords, 4:] = vector
        X[cords, 3] = 1
        cords = []
        # ones column update
        for i in range(len(X)):
            if not np.allclose(X[i, 4:], np.zeros(3)):
                X[i,3] = 1
            else:
                X[i,3] = 0
    return X


####################--- Open File Dialog ---##########################
os.chdir('./_cif')

root = tk.Tk()
root.withdraw()
root.filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select .cif File")

try:
    cif = root.filename.replace("\\", "/").split("/")[-1]
except:
    raise ValueError("No File Selected")

if cif[-4:] != ".cif":
    raise ValueError("File selected of wrong type")

#####################--- Load Structure and build X matrix ---########################
mno = loadStructure(cif).xyz.T
X = np.zeros((len(mno[0]), 7))
X[:,0], X[:,1], X[:,2] = mno[0], mno[1], mno[2]

#####################--- Save Matrix and params/title & default vector ---#############
os.chdir('../temp')
with open('points.npy', 'wb') as f:
    np.save(f, X)
    np.save(f, 4)
    np.save(f, 50)
    np.save(f, cif)
with open('vector.npy', 'wb') as f:
    np.save(f, np.array([0,0,0]))

########################--- Delete End Trigger before iterating ---#################
if os.path.exists("done.npy"):
    os.remove('done.npy')

# iterate
while not os.path.exists("done.npy"):
    # move to auxiliary .py files
    os.chdir('../aux')
    #plot in other file
    os.system('python3 inter_plot.py')
    # check if we assign vectors / end the program
    os.chdir('../temp')
    if os.path.exists("done.npy"):
        break
    with open('vector.npy', 'rb') as f:
        vector = np.load(f)
    if len(vector) != 1:
        #if we need other vectors, then run GUI
        os.chdir('../aux')
        os.system('python3 window.py')
        os.chdir('../temp')
        with open('vector.npy', 'rb') as f:
             vector = np.load(f)
    
    #load results from other executed code to get associated cords
    with open('cords.npy', 'rb') as f:
        cords = np.load(f)
        undone = list(set(np.load(f)))
        k = np.load(f)
        s = np.load(f)

    # delete temp files
    os.remove('cords.npy')

    # Update X Matrix to erase undone vectors and update new vectors    
    X = update(X, vector, np.array(cords), np.array(undone))

    # save X matrix to go back into plot
    with open('points.npy', 'wb') as f:
        np.save(f, X)
        np.save(f, k)
        np.save(f, s)
        np.save(f, cif)


