
# imports
import os
import pickle
import numpy as np
from diffpy.structure import loadStructure
from viewer.magview import MagView
from diffpy.mpdf.magstructure import MagSpecies, MagStructure 
import helpers as help

def run():   

    nonmag = []

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

    if option == "2": 
        mags = help.control_element_selection(elems, element_inx)
        X, orig_inx, nonmag, Xelem = help.split_up_magnetics(row_element, mags, struc)
    elif option == "1":
        mags = help.control_row_selection(num_el, struc_str)
        X, orig_inx, nonmag, Xelem = help.split_up_magnetics(np.arange(1,1+len(struc)), mags, struc)

    if len(nonmag) != 0:
        MagView(X, cif_name, nonmag = nonmag, basis=struc_ob.lattice.stdbase)
    else:
        MagView(X, cif_name, basis = struc_ob.lattice.stdbase)
    
    with open('X.npy', 'rb') as f:
        X = np.load(f,allow_pickle=True)
        props = np.load(f,allow_pickle=True)[0]

    magspecs = []
    labels = []
    for i in range(len(X)):
        if X[i,3] == 1:
            labels += [str(i)]
            inxs = [orig_inx[i]]
            magspecs += [MagSpecies(struc=struc_ob, label=str(i), magIdxs=inxs, basisvecs=X[i,4:7], kvecs=props[i])]

    mag = MagStructure(struc=struc_ob, species=dict(zip(labels, magspecs)))
    
    with open('mag_output.pkl', 'wb') as f:
        pickle.dump(mag, f,pickle.HIGHEST_PROTOCOL)
    
    
run()
