import ase 
from ase.io import read, write  
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

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

def plot_dos(e_range=4.0, file_name="work.dos"):
    """
    Plots the density of states from Quantum Espresso output files.
    Input: file_name (str) - the base name of the Quantum Espresso output files (without extension)
           e_range (float) - the energy range around the Fermi energy to plot
    Output: a plot of the density of states, saved as a PDF file
    """
    with open(f"{file_name}") as f:
        first_line = f.readline()
        e_fermi = float(first_line.split()[8])
    energy_limits = [e_fermi - e_range, e_fermi + e_range]
    dos = np.genfromtxt(f"{file_name}", skip_header=1) 

    fig, ax = plt.subplots(1, 1)
    ax.plot(dos[:, 0], dos[:, 1], color = "k") 
    ax.axvline(e_fermi, linestyle='dashed', color = "k") # fermi energy as horizontal line
    ax.set_xlim(energy_limits)
    ax.set_ylim(0, 1.2 * max(dos[:, 1]))
    ax.set_ylabel("number of states")
    ax.tick_params(labelleft=False, left=False)
    fig.savefig(f"dos.pdf", bbox_inches='tight') # save the figure as a pdf
    plt.show() # show the figure
    return()


def effective_mass(file_name, number_of_bands, band_index, lattice_constant=3.18e-10):
    """ 
    Calculate the effective mass of an electron in a band using a parabolic fit to the band structure.
    Inputs: file_name: the name of the file containing the band structure data
            number_of_bands: the total number of bands in the file
            band_index: the index of the band for which to calculate the effective mass (0-based)
            lattice_constant: the lattice constant of the material in meters (default is 3.18e-10 m for MoS2)
    Output: the effective mass in units of the electron mass (m_e)
    """ 
    hbar = 1.0545718e-34  # J s
    m_e = 9.10938356e-31  # kg
    ev = 1.60218e-19  # J

    bands = np.genfromtxt(file_name) 
    bands = np.split(bands, number_of_bands) 
    
    # helper function for the parabolic fit
    def parabola(k, E0, curvature_half):
        return E0 + curvature_half * k**2
    
    k_SI = bands[band_index][:, 0] * (2 * np.pi / lattice_constant)  # convert to 1/m
    E_J = bands[band_index][:, 1] * ev  # convert from eV to J
    popt, _ = curve_fit(parabola, k_SI, E_J)
    curvature = 2 * popt[1] # curvature is 2 * curvature_half
    m_eff = hbar**2 / curvature

    return m_eff / m_e
