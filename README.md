MagBuilder:
-
A simple GUI to create MagStructure objects for use in the diffpy.mpdf package (https://github.com/FrandsenGroup/diffpy.mpdf) for magnetic pair distribution function analysis. Developed by Caleb Dame (@calebdame) under the supervision of Ben Frandsen (@benfrandsen) at Brigham Young University.

Necessary libraries (not included as a standard module):
-
- diffpy.mpdf
- numpy
- matplotlib version 3.1.2
- PyQT5

Standard modules imported:
-
- os
- sys
- tkinter
- pickle

Recommended installation procedures using conda:
-
- Create a conda environment
 <pre>conda create --name mpdf python=3</pre>
- Activate the python environment
 <pre>conda activate mpdf</pre>
- Install matplotlib
 <pre>conda install matplotlib</pre>
- Install diffpy-cmi
<pre>conda install -c diffpy diffpy-cmi</pre>
- Install diffpy-mpdf by downloading the package from https://github.com/FrandsenGroup/diffpy.mpdf, navigating to the main directory of the repository, and executing 
<pre>python setup.py install</pre>

The full diffpy.mpdf package is now installed and you can run the MagBuilder program according to the instructions given below.

Instructions to run:
-
1. Place structure file (.cif file) in \_cif folder _(this is the default folder opened to load a .cif file - Files from elsewhere can be loaded once navigated to)_
2. Run run.py in conda environment with diffpy installed

Instructions to use:
- 
1. Select file either in \_cif folder or another folder
2. Decide which atoms can be selected, either individually or by atom type
3. In the viewer, assign the atoms with spins (press i in viewer to see controls)
4. In in popup, one can assign a spin to all the atoms selected and optionally include a non-unit magnitude or non-zero propagation vector
5. Upon closing the viewer by pressing close or escape, the spins, magnitudes, and propagation vectors are saved as a MagStructure Object (diffpy.magpdf) as mag_output.pkl
6. Read object into existing code with 

 <pre>with open('/path/to/mag_output.pkl', 'rb') as f:
    mag = pickle.load(f)
    f.close()</pre>


