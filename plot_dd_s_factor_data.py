"""
----------------------
Title
----------------------

Brief description of script

:Date: """

import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
from dd_cross_section.pysrc.utils import get_processed_data, sort_data


def main():

    repo_location = "/home/peter/code/src/python_code/"
    path_to_data = repo_location + "dd_cross_section/data/processed/dd_n3He/"

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
    _, ax = plt.subplots(figsize=(8, 6))
    cmap = cm.get_cmap("jet")
    plt_colours = [cmap(i) for i in np.linspace(0, 1.0, len(data_files))]

    # Loop over files
    count = 0  # for plot colours
    energy_cm_all, s_factor_all, s_factor_error_all = [], [], []
    for label, data_file in data_files.items():

        energy_cm, s_factor, s_factor_error = get_processed_data(path_to_data + data_file)
        energy_cm_sort, s_factor_sort, s_factor_error_sort = sort_data(energy_cm, s_factor, s_factor_error)
        ax.errorbar(energy_cm_sort, s_factor_sort, yerr=s_factor_error_sort, marker="o", lw=0, elinewidth=1,
                    capsize=5, label=label, color=plt_colours[count], markersize=2.5)

        energy_cm_all += energy_cm_sort
        s_factor_all += s_factor_sort
        s_factor_error_all += s_factor_error_sort
        count += 1
    #
    # energy_cm_all_sort, s_factor_all_sort, s_factor_error_all_sort = sort_data(energy_cm_all, s_factor_all,
    #                                                                            s_factor_error_all)

    # ax.errorbar(energy_cm_all_sort, s_factor_all_sort, yerr=s_factor_error_all_sort, marker="o", lw=0,
    #             elinewidth=1, capsize=5, markersize=2.5)
    #
    # # fit to data
    # fit_orders = np.arange(2, 6, 1)
    # x_fit = np.linspace(min(energy_cm_all_sort) - 1e3, max(energy_cm_all_sort) + 1e4, 5e3)
    # for fit_order in fit_orders:
    #     coefs = np.polyfit(energy_cm_all_sort, s_factor_all_sort, fit_order,
    #                        w=1/np.array(s_factor_error_all_sort))
    #     y_fit = np.polyval(coefs, x_fit)
    #     ax.plot(x_fit, y_fit)
    #
    # plt.show()

    # Finish up
    ax.set_xlim(1, 2e4)
    ax.set_ylim(0.025, 2)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel(r"$E_{\mathrm{CM}}$ [keV]")
    ax.set_ylabel("$S$ [MeV.barn]")
    plt.legend(loc="upper left", frameon=False, fontsize=8)
    plt.tight_layout()
    # plt.savefig("/home/peter/data/pa_data/dd_cross_section_work/dd_pt_s_factor_data_comp.png")
    plt.show()

    # Save data
    # np.savetxt("~/analysis/personal/dd_cross_section/" + "dd_n3he_s_factor_all_data.csv",
    #            np.transpose([energy_cm_all_sort, s_factor_all_sort, s_factor_error_all_sort]),
    #            delimiter=", ",
    #            header="E_CM [keV], S [MeV.barn], S_error [MeV.barn]")


if __name__ == "__main__":

    main()
