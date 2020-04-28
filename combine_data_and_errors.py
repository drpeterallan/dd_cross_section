"""
----------------------
combine data and errors
----------------------

Script to take data thiefed points and errors and combine into 1 file

:Date: 16/07/19
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from glob import glob


def get_data(path_to_file):
    data = pd.read_csv(path_to_file, header=0, delimiter=",")
    energy = np.array(data.iloc[:, 0].values)
    s_factor = np.array(data.iloc[:, 1].values)

    # Convert data to MeV.barn
    header = list(data.head())
    if header[1].split(".")[0].split("[")[1] == "keV":
        s_factor /= 1e3

    return np.array(energy), np.array(s_factor)


def sort_data(x_array, y_array):
    """
    Function to sort to one array based on order of another

    Parameters
    ----------
    x_array: array_like
        array containing x axis data
    y_array: array_like
        array containing y axis data

    Returns
    -------
    x_array_sort: ndarray
        ascending x values
    y_array_sort: ndarray
        y values sorted based on x_array
    """

    # Could use np.argsort()
    y_array_sort = [x for _, x in sorted(zip(x_array, y_array))]
    x_array_sort = sorted(x_array)

    return np.array(x_array_sort), np.array(y_array_sort)


def main():

    working_directory = "/home/peter/data/pa_data/dd_cross_section_work/data/dd_n3he/"
    name = "blair"
    data_file = "dd_n3he_s_factor_fig24_" + name + "_data.csv"
    error_file = "dd_n3he_s_factor_fig24_" + name + "_errors.csv"
    file_list = [working_directory + data_file, working_directory + error_file]

    for file in file_list:

        if file.split(".")[-2].split("/")[-1].split("_")[-1] == "data":
            energy, s_factor = get_data(file)
            energy_sort, s_factor_sort = sort_data(energy, s_factor)
        elif file.split(".")[-2].split("/")[-1].split("_")[-1] == "errors":
            energy_error, s_factor_error = get_data(file)
            energy_error_sort, s_factor_error_sort = sort_data(energy_error, s_factor_error)
            error = abs(s_factor_sort - s_factor_error_sort)

    plt.errorbar(energy_sort, s_factor_sort, yerr=error, marker="o", lw=0, elinewidth=1)
    plt.show()

    np.savetxt(working_directory + data_file.split(".")[0] + "_combined.csv",
               np.transpose([energy_sort, s_factor_sort, error]), delimiter=",",
               header="E_CM [keV], S [MeV.barn], S_error [MeV.barn]")


if __name__ == "__main__":

    main()
