"""
-----------------------
combine data and errors
-----------------------

Data points and their corresponding errors are captured separately using web plot digitizer. Script reads files and
combines into a single file with structure: energy, s-factor, s-factor error

Note, data was gathered incrementally from plots in papers hence this was performed on a file by file basis.

Date: 16/07/19
Author: P. Allan
"""

import matplotlib.pyplot as plt
from dd_cross_section.pysrc.utils import get_wpd_data
from dd_cross_section.pysrc.utils import sort_data
import numpy as np


def main(data_file="dd_n3he_s_factor_fig24_blair_data.csv",
         error_file="dd_n3he_s_factor_fig24_blair_errors.csv",
         debug=True):

    path_to_data = "../data/raw/wpd_s_factor_data/dd_n3he/"
    file_list = [path_to_data + data_file, path_to_data + error_file]

    for file in file_list:

        if file.split(".")[-2].split("/")[-1].split("_")[-1] == "data":
            energy, s_factor = get_wpd_data(file)
            energy_sort, s_factor_sort = sort_data(energy, s_factor)
        elif file.split(".")[-2].split("/")[-1].split("_")[-1] == "errors":
            energy_error, s_factor_error = get_wpd_data(file)
            energy_error_sort, s_factor_error_sort = sort_data(energy_error, s_factor_error)
            error = abs(s_factor_sort - s_factor_error_sort)

    if debug:
        plt.errorbar(energy_sort, s_factor_sort, yerr=error, marker="o", lw=0, elinewidth=1, capsize=2, capthick=0.5,
                     color="blue")
        plt.xlabel("Energy [keV]")
        plt.ylabel("$S$ [MeV.barn]")
        plt.show()

    np.savetxt("../data/processed/dd_n3he/" +
               data_file.split(".")[0] + "_combined.csv",
               np.transpose([energy_sort, s_factor_sort, error]), delimiter=",",
               header="E_CM [keV], S [MeV.barn], S_error [MeV.barn]")


if __name__ == "__main__":

    main(data_file="dd_n3he_s_factor_fig24_blair_data.csv",
         error_file="dd_n3he_s_factor_fig24_blair_errors.csv",
         debug=False)
