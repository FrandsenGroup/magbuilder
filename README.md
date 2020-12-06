A demo of how to visualize 3d mulecular structures and iteratively select and interface with individual atoms to save and visualize magnetic spins.  To be integrated into PDFgui, a part of the larger diffpy aparatus

Necessary libraries:
- diffpy/Structure
- numpy
- matplotlib
- PyQT5

Instructions:
1. Place .cif file in _cif folder
2. Enter file name in plot.py file
3. Run plot.py in conda environment with diffpy installed

Visualization Controls:
- Left click to select atoms to which a spin is added, left click to undo
- Once all atoms to have spins added are selected, close the window or press enter
- The popup will prompt user for dx,dy,dz vector coordinates for the selected atoms.  Press Enter or Set Spins to set.  Cancel to not set spins.
- To undo a made spin, righ click on the red vectorized atom
