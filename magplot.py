
# imports
import os
import pickle
from tkinter import filedialog
import tkinter as tk
import numpy as np
from diffpy.structure import loadStructure
from viewer.magview import MagView
from diffpy.mpdf.magstructure import MagSpecies, MagStructure 

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
    ########### check right file type
    if cif[-4:] != ".cif":
        raise ValueError("File selected of wrong type. Must select a .cif file")
    
    #### load as diffpy.structure object
    struc_ob = loadStructure(cif)
    struc = struc_ob.xyz_cartn.T
    element_inx = struc_ob.element
    
    #### print structure
    print("\nCif file:")
    print(struc_ob)
    print("")
    # input 1, 2, or exit 
    option = input("Enter \n1: to select magnetic atoms individually, \n2: to select by element type\n\n").replace(" ","")
    while 1:  
        # control for other inputs
        if "exit" in option:
            print("Program Aborted")
            return 0
        if option =="1" or option == "2":
            break
        option = input("Invalid Input.  \nValid inputs are 'exit', '1', or '2'\n\n").replace(" ","")

    print("")
    nonmag = []

    if option == "2": 
        # select magnetic atoms by element type
        
        # display elements and indeces
        elems = list(set(struc_ob.element))
        elems.sort()
        inx = np.arange(1,1+len(elems))
        dmap = dict(zip(elems, inx))
        for i in range(len(elems)):
            print(str(i + 1) + '\t' + elems[i])
        mags = input("\nEnter the index of each magnetic element (delimited by commas)\n").replace(" ","").split(",")

        # control for other inputs
        while 1:
            if "exit" in mags:
                print("Program Aborted")
                return 0
            if set(mags).issubset(set(inx.astype(str))):
                break
            mags = input("Invalid Input.  \nValid inputs are 'exit', or the integer range between "+str(inx[0]) + ", and " +str(inx[-1])+"\n").replace(" ","").split(",")
        
        ####--- Build matrix and load viewer ---#####
    
        X = []
        Z = np.array([struc[0], struc[1], struc[2]]).T
        originx = []
        
        # separate 
        for i in range(len(Z)):
            if str(dmap[element_inx[i]]) in mags:
                X += [Z[i,:]]
                originx += [i]
            else:
                nonmag += [Z[i,:]]
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
    
        X = []
        Z = np.array([struc[0], struc[1], struc[2]]).T
        originx = []

        for i in range(len(Z)):
            if str(i) in mags:
                X += [Z[i,:]]
                originx += [i]
            else:
                nonmag += [Z[i,:]]
    if len(nonmag) != 0:
        MagView(np.array(X), cif, els = struc_ob.element, nonmag = np.array(nonmag)[:,:3], basis=struc_ob.lattice.stdbase)
    else:
        MagView(np.array(X), cif, els = struc_ob.element, basis = struc_ob.lattice.stdbase)
    
    with open('X.npy', 'rb') as f:
        X = np.load(f)
    os.remove('X.npy')
    
    X = np.concatenate([X, np.array(originx).reshape(len(originx),1)], axis=1)
    
    magspecs = []
    labels = []
    for i in np.unique(X[:,8]):
        if i != 0:
            spec = X[X[:,8]==i,: ]
            labels += [str(i)]
            inxs = list(set(spec[:,-1]))
            magspecs += [MagSpecies(struc=struc_ob, label=str(i), magIdxs=inxs, basisvecs=spec[0,4:7].reshape(1,3), kvecs= spec[0,9:12].reshape(1,3))]
    mag = MagStructure(struc=struc_ob, species=dict(zip(labels, magspecs)))
    
    with open('mag_output.pkl', 'wb') as f:
        pickle.dump(mag, f,pickle.HIGHEST_PROTOCOL)
    
    
run()
