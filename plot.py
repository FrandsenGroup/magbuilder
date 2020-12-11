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
import matplotlib as mpl

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


mno = loadStructure(cif).xyz.T
x = mno[0]
y = mno[1]
z = mno[2]

cords_list = []
vector_list = []

# move to temp and save structure and title
os.chdir('../temp')
with open('points.npy', 'wb') as f:
    np.save(f, x)
    np.save(f, y)
    np.save(f, z)
    np.save(f, cif)
quiver = np.zeros((len(x), 3))
# save data to show which cords have what vectors
with open('arrows.npy', 'wb') as f:
    np.save(f, [], allow_pickle=True)
    np.save(f, quiver, allow_pickle=True)
    np.save(f, 4, allow_pickle=True)
# delete file to end program
if os.path.exists("done.npy"):
    os.remove('done.npy')

while not os.path.exists("done.npy"):
    # move to auxiliary .py files
    os.chdir('../aux')
    #plot in other file
    os.system('python3 inter_plot.py')
    #gui in other file
    os.system('python3 window.py')
    os.chdir('../temp')

    if os.path.exists("done.npy"):
        break
    
    last_cords = []

    #load results from other executed code to get vector and associated cords
    with open('cords.npy', 'rb') as f:
        cords = np.load(f)
        k = np.load(f)

    with open('vector.npy', 'rb') as f:
        vector = np.load(f)

    # delete temp files
    os.remove('vector.npy')
    os.remove('cords.npy')
    if len(vector) != 1:
        vector = vector / la.norm(vector)
        # save list of cords assigned a vector and respective vectors
        quiver[np.array(cords), :] = vector.ravel()
        last_cords = cords
    else:
        cords = last_cords
    with open('arrows.npy', 'wb') as f:
        np.save(f, cords, allow_pickle=True)
        np.save(f, quiver, allow_pickle=True)
        np.save(f, k, allow_pickle=True)

os.remove('arrows.npy')
os.remove('points.npy')
