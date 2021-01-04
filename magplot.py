
# imports
import os
from tkinter import filedialog
import tkinter as tk
import numpy as np
from diffpy.structure import loadStructure
from viewer.magview import MagView

def run():   

    ####################--- Open File Dialog ---##########################
    os.chdir('./_cif')

    root = tk.Tk()
    root.withdraw()
    
    ####--- Read structure --####
    try:
        root.filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select .cif File")
        cif = root.filename.split("/")[-1]
        struc_ob = loadStructure(cif)
         
    except:
        print("Must Select .cif file")
        return 0

    if cif[-4:] != ".cif":
        raise ValueError("File selected of wrong type")

    struc_ob = loadStructure(cif)
    struc = struc_ob.xyz.T
    element_inx = struc_ob.element
    
    print("\nCif file:")
    print(struc_ob)
    print("")
    option = input("Enter \n1: to select magnetic atoms individually, \n2: to select by element type\n\n").replace(" ","")
    while 1:  
        if "exit" in option:
            print("Program Aborted")
            return 0
        if option =="1" or option == "2":
            break
        option = input("Invalid Input.  \nValid inputs are 'exit', '1', or '2'\n\n").replace(" ","")

    print("")

    if option == "2":
        elems = list(set(struc_ob.element))
        elems.sort()
        inx = np.arange(1,1+len(elems))
        dmap = dict(zip(elems, inx))
    
        for i in range(len(elems)):
            print(str(i + 1) + '\t' + elems[i])
        mags = input("\nEnter the index of each magnetic element (delimited by commas)\n").replace(" ","").split(",")
        while 1:
            if "exit" in mags:
                print("Program Aborted")
                return 0
            if set(mags).issubset(set(inx.astype(str))):
                break
            mags = input("Invalid Input.  \nValid inputs are 'exit', or the integer range between "+str(inx[0]) + ", and " +str(inx[-1])+"\n").replace(" ","").split(",")
        
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
    elif option == "1":
        struc_str = str(struc_ob).split("\n")
        for i in np.arange(1,len(struc.T)+1):
            print(str(i)+"\t"+struc_str[i])

        mags = input("\nEnter the index of each magnetic atom (delimited by commas)\n").replace(" ","").split(",")
        while 1:
            if "exit" in mags:
                print("Program Aborted")
                return 0
            if set(mags).issubset(set(np.arange(1,len(struc.T)+1).astype(str))):
                break
            mags = input("Invalid Input.  \nValid inputs are 'exit', or the integer range between '1'" + ", and '" +str(len(struc.T))+"'\n")
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
    if len(others) != 0:
        return MagView(np.array(X), cif, 4, 50, np.array(others)[:,:3])
    else:
        return MagView(np.array(X), cif, 4, 50)

run()
