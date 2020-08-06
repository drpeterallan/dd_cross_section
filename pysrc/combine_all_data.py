"""
-----------------------
combine_all_data.py
-----------------------

Take individual processed files from wpd and combine into single sorted data file

Date: 16/07/19
Author: P. Allan
"""

from dd_cross_section.pysrc.utils import get_processed_data, sort_data
import numpy as np
from glob import glob
import os


def main():

    path_to_data = "../data/processed/dd_n3he/"
    data_files = glob(path_to_data + "*_combined.csv")

    # Loop over files and combine data
    energy_cm_all, s_factor_all, s_factor_error_all = [], [], []
    for data_file in data_files:
        energy_cm, s_factor, s_factor_error = get_processed_data(data_file)
        energy_cm_sort, s_factor_sort, s_factor_error_sort = sort_data(energy_cm, s_factor, s_factor_error)
        energy_cm_all = np.append(energy_cm_all, energy_cm_sort)
        s_factor_all = np.append(s_factor_all, s_factor_sort)
        s_factor_error_all = np.append(s_factor_error_all, s_factor_error_sort)

    # Sort and save combined data
    energy_cm_all_sort, s_factor_all_sort, s_factor_error_all_sort = sort_data(energy_cm_all, s_factor_all,
                                                                               s_factor_error_all)
    np.savetxt("../data/processed/dd_n3he/dd_n3he_s_factor_all_data.csv",
               np.transpose([energy_cm_all_sort, s_factor_all_sort, s_factor_error_all_sort]),
               header="E_CM [keV], S [MeV.barn], S_error [MeV.barn]",
               delimiter=", ")


if __name__ == "__main__":
    main()
