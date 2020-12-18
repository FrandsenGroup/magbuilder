
# imports
import os
from tkinter import filedialog
import tkinter as tk
import numpy as np
from diffpy.structure import loadStructure
from viewer.magview import MagView


####################--- Open File Dialog ---##########################
os.chdir('./_cif')

root = tk.Tk()
root.withdraw()
root.filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select .cif File")

####--- Read structure --####

try:
    cif = root.filename.replace("\\", "/").split("/")[-1]
except:
    raise ValueError("No File Selected")

if cif[-4:] != ".cif":
    raise ValueError("File selected of wrong type")

struc = loadStructure(cif).xyz.T

####--- Build matrix and load viewer ---#####

X = np.zeros((len(struc[0]), 7))
X[:,0], X[:,1], X[:,2] = struc[0], struc[1], struc[2]

MagView(X, cif, 4, 50)

