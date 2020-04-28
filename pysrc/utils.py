"""
-----------------------
utils.py
-----------------------

Generic functions for reading and processing etc.

Date: 28/04/2020

"""

import pandas as pd
import numpy as np


def get_wpd_data(path_to_file):
    """
    Function for reading output from web plot digitizer

    Parameters
    ----------
    path_to_file: basestring
        location of data

    Returns
    -------
    energy: array_like
        array of energies in keV
    s_factor: array_like
        array of astrohpyical factors in MeV barn
    """

    data = pd.read_csv(path_to_file, header=0, delimiter=",")
    energy = np.array(data.iloc[:, 0].values)
    s_factor = np.array(data.iloc[:, 1].values)

    # Convert data to MeV.barn
    header = list(data.head())
    if header[1].split(".")[0].split("[")[1] == "keV":
        s_factor /= 1e3

    return np.array(energy), np.array(s_factor)


def get_processed_data(path_to_file):
    data = pd.read_csv(path_to_file, header=0, delimiter=",")
    energy = np.array(data.iloc[:, 0].values)
    s_factor = np.array(data.iloc[:, 1].values)
    s_factor_error = np.array(data.iloc[:, 2].values)

    header = list(data.head())
    if header[1].split(".")[0].split("[")[1] == "keV":
        s_factor /= 1e3
        s_factor_error /= 1e3

    return energy, s_factor, s_factor_error


def sort_data(x_array, y_array, y_error=None):
    """
    Function to sort to one array based on order of another

    Parameters
    ----------
    x_array: array_like
        array containing x axis data
    y_array: array_like
        array containing y axis data
    y_error: array_like (default none)
        array containing error bars

    Returns
    -------
    x_array_sort: list
        ascending x values
    y_array_sort: list
        y values sorted based on x_array
    """
    y_array_sort = np.array([x for _, x in sorted(zip(x_array, y_array))])
    x_array_sort = np.array(sorted(x_array))

    if y_error is not None:
        y_error_sort = np.array([x for _, x in sorted(zip(x_array, y_error))])
        return x_array_sort, y_array_sort, y_error_sort
    else:
        return x_array_sort, y_array_sort
