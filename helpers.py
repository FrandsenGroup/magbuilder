from tkinter import filedialog
import tkinter as tk
import os
import numpy as np

def get_file():
    os.chdir('./input')
    root = tk.Tk()
    root.withdraw()
    root.filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select structure file")
    return root.filename

def check_file(filename):
    try:
        print(filename)
        fname = filename.split("/")[-1]
        extension = fname.split(".")[-1]
        print(extension)
    except:
        raise ValueError("File selected of wrong type. Must select a .cif or .stru file")
    if extension not in ['cif', 'stru']:
        raise ValueError("File selected of wrong type. Must select a .cif or .stru file")
    return fname

def control_selection_technique(option):
    while 1:  
        # control for other inputs
        if "exit" in option:
            raise ValueError("Program Aborted")
        if option =="1" or option == "2":
            break
        option = input("Invalid Input.  \nValid inputs are 'exit', '1', or '2'\n\n").replace(" ","")
    return option   

def control_element_selection(elems,element_inx):
    # display elements and indeces
    for i in range(len(elems)):
        print(str(i + 1) + '\t' + elems[i])
    mags = input("\nEnter the index of each magnetic "
                +"element (delimited by commas)\n").replace(" ","").split(",")

    # control for other inputs
    while 1:
        if "exit" in mags:
            raise ValueError("Program Aborted")
            
        if set(mags).issubset(set(element_inx.astype(str))):
            break
        mags = input("Invalid Input.  \nValid inputs are 'exit', "
                      +"or the integer range between "+str(element_inx[0]) 
                      +", and " +str(element_inx[-1])+"\n").replace(" ","").split(",")
    return mags


def control_row_selection(num_el, struc_str):

    for i in np.arange(1,num_el+1):
        print(str(i)+"\t"+struc_str[i])

    mags = input("\nEnter the index of each magnetic atom (delimited by commas)\n").replace(" ","").split(",")
    while 1:
        if "exit" in mags:
            print("Program Aborted")
            return 0
        if set(mags).issubset(set(np.arange(1,num_el+1).astype(str))):
            break
        mags = input("Invalid Input.  \nValid inputs are 'exit', or the integer "
                +"range between '1'" + ", and '" +str(num_el)+"'\n")
        mags = mags.replace(" ","").split(",")
    return mags

def split_up_magnetics(cond, mags, struc, row_element):
    X, orig_inx, nonmag, Xelem = [], [], [], []
    for i in range(len(struc)):
        if str(cond[i]) in mags:
            X += [struc[i,:]]
            orig_inx += [i]
            Xelem += [row_element[i]]
        else:
            nonmag += [struc[i,:]]
    return np.array(X), np.array(orig_inx), np.array(nonmag), np.array(Xelem)



