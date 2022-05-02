MagBuilder:
-
A simple GUI to create MagStructure objects for use in the diffpy.mpdf package (https://github.com/FrandsenGroup/diffpy.mpdf) for magnetic pair distribution function analysis. Developed by Caleb Dame (@calebdame) under the supervision of Ben Frandsen (@benfrandsen) at Brigham Young University.

Dependencies:
-
- diffpy.mpdf
- numpy
- matplotlib version 3.1.2
- PyQT5

Recommended installation procedures using conda:
-
- Create a conda environment
 <pre>conda create --name magbuilder python=3</pre>
- Activate the python environment
 <pre>conda activate mpdf</pre>
- Install matplotlib
 <pre>conda install matplotlib</pre>
- Install diffpy-cmi
<pre>conda install -c diffpy diffpy-cmi</pre>
- Install diffpy-mpdf by downloading the package from https://github.com/FrandsenGroup/diffpy.mpdf, navigating to the main directory of the repository, and executing 
<pre>python setup.py install</pre>

The full diffpy.mpdf package is now installed and you can run the MagBuilder program according to the instructions given below. (Note, however, that the older version of Matploblib used here causes problems for one of the visualization features in diffpy.mpdf, so it may be best to use two different environments, one for MagBuilder and the other for the main diffpy.mpdf package.)

Usage:
-
1. Download this repository and store it wherever you like on your local machine
2. Place structure file (.cif or .stru file) in the input folder of your copy of the repository
3. Activate the magbuilder conda environment, navigate to your copy of the respository, and run magbuilder.py
4. Follow the prompt to select a structure file from the input folder
5. Specify the magnetic atoms, either individually or by atomic species
6. In the interactive viewer, select the appropriate atoms and set the magnetic information (press i in viewer to see controls)
7. Upon closing the viewer, a MagStructure object is saved as a binary file with a user-defined name in the output folder
8. Using a python script or jupyter notebook, the MagStructure object can be opened up for further use as shown below: 

 <pre>with open('/path/to/mag_output.pkl', 'rb') as f:
    mag = pickle.load(f)
    f.close()</pre>

The example.ipynb notebook included in this repository provides a simple example of this functionality.
