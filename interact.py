import sys
import os
import numpy.linalg as la
import numpy as np 
import time
from matplotlib import pyplot as plt
from diffpy.structure import loadStructure
from mpl_toolkits.mplot3d import Axes3D

# name of cif file in folder
cif = 'MnO_R-3m'
# get structure
mno = loadStructure(cif + '.cif').xyz.T
x = mno[0]
y = mno[1]
z = mno[2]

with open('points.npy', 'wb') as f:
    np.save(f, x)
    np.save(f, y)
    np.save(f, z)
    np.save(f, cif)
with open('vector.npy', 'wb') as f:
    np.save(f, np.ones(3))

#plot in other file
os.system('python3 inter_plot.py')
#gui in other file
os.system('python3 window.py')

#load results from other executed code
with open('cords.npy', 'rb') as f:
    cords = np.load(f)
with open('vector.npy', 'rb') as f:
    vector = np.load(f)

# delete files
os.remove('vector.npy')
os.remove('cords.npy')
os.remove('points.npy')

#format plot with arrows
vector = vector / (3*la.norm(vector))
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
ax.scatter(x,y,z, color="blue", s=55)
plt.quiver(cords[:,0], cords[:,1], cords[:,2], vector[0], vector[1], vector[2], length=(np.max(x) - np.min(x))/1.5, color="black")
plt.show()
