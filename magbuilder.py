# imports
import os
import pickle
import numpy as np
from diffpy.mpdf import *
from diffpy.structure import loadStructure
from viewer.magview import MagView
import helpers as help

def run():   
    """ Main program operation.
    """
    nonmag = []
    os.chdir("./input")
    try:
        os.remove('data.npy')
    except:
        already_deleted = True
    os.chdir("..")
    
    ####--- Read structure --####
    filepath = help.get_file()
    cif_name = help.check_cif(filepath)
    #### load as diffpy.structure object
    struc_ob = loadStructure(cif_name)
    struc = struc_ob.xyz_cartn
    
    ## convenient data saved as variables
    elems = list(set(struc_ob.element))
    elems.sort() 				# alphabetical list of elements
    element_inx = np.arange(1,1+len(elems)) 		# 1 to n+1 indeces for each element
    dmap = dict(zip(elems, element_inx)) 		# element name to associated number
    revdmap = dict(zip(element_inx, elems))
    row_element = np.array([dmap[i] for i in struc_ob.element])
    struc_str = str(struc_ob).split("\n") 	# print string
    num_el = len(struc)

    #### print structure
    print("\nCif file:")
    print(struc_ob)
    print("")
    # input 1, 2, or exit 
    prelim_input = input("Enter \n1: to select magnetic atoms individually," 
                                + "\n2: to select by element type\n\n").replace(" ","")
    option = help.control_selection_technique(prelim_input)
    print("")
    # either select by element type, or by individual index
    if option == "2": 
        mags = help.control_element_selection(elems, element_inx)
        X, orig_inx, nonmag, Xelem = help.split_up_magnetics(row_element, mags, struc, row_element)
    elif option == "1":
        mags = help.control_row_selection(num_el, struc_str)
        X, orig_inx, nonmag, Xelem = help.split_up_magnetics(np.arange(1,1+len(struc)), mags, struc, row_element)
    # save data and build viewer object
    if len(nonmag) != 0:
        with open('data.npy', 'wb') as f:
            np.save(f, X)
            np.save(f, Xelem)
            np.save(f, revdmap)
            np.save(f, nonmag)
            np.save(f, cif_name)
            np.save(f, struc_ob.lattice.stdbase)

        MagView(X, Xelem, revdmap, nonmag = nonmag, cif=cif_name,  basis=struc_ob.lattice.stdbase)
    else:
        with open('data.npy', 'wb') as f:
            np.save(f, X)
            np.save(f, Xelem)
            np.save(f, revdmap)
            np.save(f, nonmag)
            np.save(f, cif_name)
            np.save(f, struc_ob.lattice.stdbase)
        MagView(X, Xelem, revdmap, cif=cif_name, basis = struc_ob.lattice.stdbase)

    #build MagStructure object with info collected in the viewer    

    with open('X.npy', 'rb') as f:
        X = np.load(f,allow_pickle=True)
        props = np.load(f,allow_pickle=True)[0]
    os.remove('X.npy')
    os.chdir("../input")
    os.remove('data.npy')
    os.chdir("../output")
    magspecs = []
    labels = []
    for i in range(len(X)):
        if X[i,3] == 1:
            labels += [str(i)]
            inxs = [orig_inx[i]]
            print('Index: ',orig_inx[i])
            magspecs += [MagSpecies(struc=struc_ob, label=str(i), strucIdxs=inxs, basisvecs=X[i,4:7], kvecs=props[i], origin=np.array(struc_ob[orig_inx[i]].xyz_cartn))]

    mag = MagStructure(struc=struc_ob, species=dict(zip(labels, magspecs)))
    
    # save obj to pkl file in output
    title = input("Enter alpha-numeric filename: ")
    with open(title + '.pkl', 'wb') as f:
        pickle.dump(mag, f,pickle.HIGHEST_PROTOCOL)
    print("File saved as " + title + ".pkl in output folder" )    
run()
