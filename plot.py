import os
import numpy.linalg as la
import numpy as np 
from matplotlib import pyplot as plt
from diffpy.structure import loadStructure
from mpl_toolkits.mplot3d import Axes3D
import matplotlib as mpl
mpl.rcParams['toolbar'] = 'None'

cords_list = []
vector_list = []

# name of cif file in folder
#cif = input("Enter Name of .cif file:\n")
cif =  'MnO_R-3m'

# get structure in _cif folder
os.chdir('./_cif')
mno = loadStructure(cif + '.cif').xyz.T
x = mno[0]
y = mno[1]
z = mno[2]

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

    #check if we are done or if we need to click more points
    if not os.path.exists("done.npy"):
        continue

    #format final plot with arrows
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title(cif)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.set_xlim3d((np.min(x) - (np.max(x)-np.min(x))/4, (np.max(x) + (np.max(x)-np.min(x))/4)))
    ax.set_ylim3d((np.min(y) - (np.max(y)-np.min(y))/4, (np.max(y) + (np.max(y)-np.min(y))/4)))
    ax.set_zlim3d((np.min(z) - (np.max(z)-np.min(z))/4, (np.max(z) + (np.max(z)-np.min(z))/4)))
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    X = np.concatenate([x.reshape(len(x), 1),y.reshape(len(x), 1),z.reshape(len(x), 1)], 1)
    cords = np.concatenate(cords_list)
    magset = set(zip(cords[:,0], cords[:,1], cords[:,2]))
    for i in X:
        a,b,c = i
        if (a,b,c) not in magset:
            ax.scatter(a,b,c, color="blue", s=55)
        else:
            ax.scatter(a,b,c, color="red", s=55)
    
    for i in range(len(cords_list)):
        plt.quiver(cords_list[i][:,0], cords_list[i][:,1], 
                   cords_list[i][:,2], vector_list[i][0], 
                   vector_list[i][1], vector_list[i][2], 
                   length=(np.max(x) - np.min(x))/4, color="black")
    plt.show()

os.remove('points.npy')
