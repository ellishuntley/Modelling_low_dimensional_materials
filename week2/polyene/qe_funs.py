import ase 
from ase.io import read, write  

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42
mpl.rc('font',**{'family':'sans-serif','sans-serif':['Arial']})
mpl.rcParams['font.size'] = 16

colours = {
    "green": "#00B828",
    "yellow": "#FFD900",
    "purple": "#800FF2",
    "blue": "#0073FF",
    "orange": "#FF5000",
    "grey": "#B3B3B3",
}

plt.rcParams.update({
    'xtick.major.width': 2,     # x-tick thickness
    'ytick.major.width': 2,     # y-tick thickness
    'xtick.major.size': 5,        # x-tick length
    'ytick.major.size': 5,        # y-tick length
    'axes.linewidth': 2,         # Thickness of axis border (applies to spines)
    'lines.linewidth': 2
})

def write_geom(filename):
    """
    Reads a Quantum Espresso input file and writes the atomic positions to an XSF file.
    Input: filename (str) - the full name of the Quantum Espresso input file 
    Output: ASE atoms object, function also writes an XSF file with the atomic positions
    """
    atoms = read(f"{filename}", format='espresso-in') 
    write(f"{filename}.xsf", atoms) 
    return atoms

# paste your plotting function here
