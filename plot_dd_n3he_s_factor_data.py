"""
----------------------
plot_dd_s_factor_data
----------------------

Plot all data gathered for the d + d --> n + 3He reaction

Date: 16/07/19
Author: P. Allan
"""

from dd_cross_section.pysrc.utils import get_processed_data, sort_data, set_rcParams
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import os


def main():

    path_to_data = "./data/processed/dd_n3he/"

    data_files = {
        "Arnold (1954)": "dd_n3he_s_factor_fig13_arnold_data_combined.csv",
        "Booth (1956)": "dd_n3he_s_factor_fig13_booth_data_combined.csv",
        "Brown (1989)": "dd_n3he_s_factor_fig13_brown_data_combined.csv",
        "McNeill (1951)": "dd_n3he_s_factor_fig14_mcneill_data_combined.csv",
        "Davidenko (1957)": "dd_n3he_s_factor_fig14_davidenko_data_combined.csv",
        "Krauss (1957)": "dd_n3he_s_factor_fig14_krauss_data_combined.csv",
        "Preston (1954)": "dd_n3he_s_factor_fig15_preston_data_combined.csv",
        "Ganeev (1957)": "dd_n3he_s_factor_fig15_ganeev_data_combined.csv",
        "Casey (2017)": "dd_n3he_s_factor_casey_data_combined.txt",
        "Bystritsky (2010)": "dd_n3he_s_factor_bystritsky_data_combined.csv",
        "Greife (1995)": "dd_n3he_s_factor_greife_data_combined.csv",
        "Schulte (1972)": "dd_n3he_s_factor_fig24_schulte_data_combined.csv",
        "Hunter (1949)": "dd_n3he_s_factor_fig24_hunter_data_combined.csv",
        "Blair (1948)": "dd_n3he_s_factor_fig24_blair_data_combined.csv",
        "Brolley (1957)": "dd_n3he_s_factor_fig25_brolley_data_combined.csv",
        "Goldberg (1960)": "dd_n3he_s_factor_fig25_goldberg_data_combined.csv",
        "Thornton (1969)": "dd_n3he_s_factor_fig25_thornton_data_combined.csv",
        "Erickson (1949)": "dd_n3he_s_factor_fig25_erickson_data_combined.csv"
    }

    # Plotting setup
    set_rcParams()
    _, ax = plt.subplots(figsize=(8, 6))
    cmap = cm.get_cmap("jet")
    plt_colours = [cmap(i) for i in np.linspace(0, 1.0, len(data_files))]

    # Loop over files
    count = 0  # for plot colours
    for label, data_file in data_files.items():

        energy_cm, s_factor, s_factor_error = get_processed_data(path_to_data + data_file)
        energy_cm_sort, s_factor_sort, s_factor_error_sort = sort_data(energy_cm, s_factor, s_factor_error)
        ax.errorbar(energy_cm_sort, s_factor_sort, yerr=s_factor_error_sort, marker="o", lw=0, elinewidth=1,
                    capsize=5, label=label, color=plt_colours[count], markersize=2.5)
        count += 1

    # Finish up
    ax.set_xlim(1, 2e4)
    ax.set_ylim(0.025, 2)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel(r"$E_{\mathrm{CM}}$ [keV]")
    ax.set_ylabel("$S$ [MeV.barn]")
    plt.legend(loc="upper left", frameon=False, fontsize=8)
    plt.tight_layout()
    plt.savefig("./data/figs/dd_n3he_s_factor_data_comp.png")
    plt.show()


if __name__ == "__main__":

    main()
