
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

struc_ob = loadStructure(cif)
struc = struc_ob.xyz.T
element_inx = struc_ob.element

print("\nCif file:")
print(struc_ob)
print("")
option = input("Enter \n1 to select magnetic atoms individually, \n2 to select by element type\n\n").replace(" ","")

if option not in {"1", "2"}:
    raise ValueError("Not valid input.")

print("")

if option == "2":
    elems = list(set(struc_ob.element))
    inx = np.arange(1,1+len(elems))
    dmap = dict(zip(elems, inx))
    
    for i in range(len(elems)):
        print(str(i + 1) + '\t' + elems[i])
    mags = input("\nEnter the index of each magnetic element (delimited by commas)\n")
    mags = mags.replace(" ","").split(",")

    ####--- Build matrix and load viewer ---#####
    
    others = []
    X = []
    Z = np.zeros((len(struc[0]), 7))
    Z[:,0], Z[:,1], Z[:,2] = struc[0], struc[1], struc[2] 
    
    for i in range(len(Z)):
        if str(dmap[element_inx[i]]) in mags:
            X += [Z[i,:]]
        else:
            others += [Z[i,:]]

else:
    struc_str = str(struc_ob).split("\n")
    for i in np.arange(1,len(struc.T)+1):
        print(str(i)+"\t"+struc_str[i])

    mags = input("\nEnter the index of each magnetic atom (delimited by commas)\n")
    mags = mags.replace(" ","").split(",")
    
    others = []
    X = []
    Z = np.zeros((len(struc[0]), 7))
    Z[:,0], Z[:,1], Z[:,2] = struc[0], struc[1], struc[2] 
    
    for i in range(len(Z)):
        if str(i) in mags:
            X += [Z[i,:]]
        else:
            others += [Z[i,:]]

MagView(np.array(X), cif, 4, 50, np.array(others)[:,:3])
