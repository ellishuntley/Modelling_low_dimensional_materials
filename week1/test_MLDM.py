# First we import a few modules and define helper functions.
import numpy as np
import matplotlib.pyplot as plt
import os


def gauss(x, x0, a, sigma):
    return a * np.exp(-((x - x0) ** 2) / (2 * sigma ** 2))


def lorentz(x, x0, a, gamma):
    return a * gamma / ((x - x0) ** 2 + gamma ** 2)


def read_csv(filename):
    """
    Reads a .csv file with two columns and returns two arrays.
    Assumes that the first row is a header.
    """
    try:
        # Make path relative to this script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(script_dir, filename)

        data = np.loadtxt(filepath, delimiter=',', skiprows=1)
        x_original = data[:, 0]
        y_original = data[:, 1]
        print(f"Loaded {len(x_original)} data points from {filepath}")
        return x_original, y_original

    except FileNotFoundError:
        raise FileNotFoundError(f"File '{filename}' not found!")

    except Exception as e:
        raise RuntimeError(f"Error reading file: {e}")


def plot_broadened_data(x, y):
    plt.figure()
    plt.plot(x, y)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()


def broaden(file_name, b_type="gauss", sigma=0.5, npoints=1000, save_csv=False):
    """
    Main function for broadening data.
    """
    # Read the csv file.
    x_original, y_original = read_csv(file_name)

    # Create broadened x and y.
    x_broadened = np.linspace(min(x_original), max(x_original), npoints)
    y_broadened = np.zeros_like(x_broadened)

    # Loop over signals.
    if b_type == "gauss":
        for i in range(len(x_original)):
            y_broadened += gauss(x_broadened, x_original[i], y_original[i], sigma)

    elif b_type == "lorentz":
        for i in range(len(x_original)):
            y_broadened += lorentz(x_broadened, x_original[i], y_original[i], sigma)

    else:
        raise ValueError(
            f"Unknown broadening type '{b_type}'. Use 'gauss' or 'lorentz'."
        )

    # Plot the broadened data.
    plot_broadened_data(x_broadened, y_broadened)

    # Optionally save a csv.
    if save_csv:
        output_data = np.column_stack((x_broadened, y_broadened))
        np.savetxt(
            "broadened_data.csv",
            output_data,
            delimiter=',',
            header='x,y_broadened'
        )

    return x_broadened, y_broadened


# Execute
file_name = "sample_peaks.csv"
broaden(file_name)