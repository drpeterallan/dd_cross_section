"""
------------------------
dd_n3he_s_factor_fitting
------------------------

Date: 06/08/2019
Author: P. Allan
"""

from dd_cross_section.pysrc.utils import get_processed_data, set_rcParams
import matplotlib.pyplot as plt
import numpy as np
import pymc3 as pm
import arviz as az
import multiprocessing as mp
from scipy.optimize import curve_fit


def pade_func(energy_array, A1, A2, A3, A4, B1, B2, B3, B4):
    return (A1 + energy_array * (A2 + energy_array * (A3 + energy_array * A4)))\
           / (1 + energy_array * (B1 + energy_array * (B2 + energy_array * (B3 + energy_array * B4))))


def lsq_fit(func, x, y):
    coefs, _ = curve_fit(pade_func, x, y)
    return coefs


def bayesian_fit(x, y, y_error, num_samples=500):

    with pm.Model() as model:

        # Setup the model
        A1 = pm.Flat("A1")
        A2 = pm.Flat("A2")
        A3 = pm.Flat("A3")
        A4 = pm.Flat("A4")
        B1 = pm.Flat("B1")
        B2 = pm.Flat("B2")
        B3 = pm.Flat("B3")
        B4 = pm.Flat("B4")
        # y_stdev = pm.HalfNormal("Y_stdev", sd=1)

        y_mean = pm.Deterministic("y_mean", pade_func(x, A1, A2, A3, A4, B1, B2, B3, B4))
        # y_pred = pm.Normal("y_pred", mu=y_mean, observed=y)
        # y_pred = pm.Normal("y_pred", mu=y_mean, sd=y_error, observed=y)
        y_pred = pm.Normal("y_pred", mu=y_mean, tau=1.0/y_error**2, observed=y)

        # Do the fitting
        start = pm.find_MAP()
        trace = pm.sample(num_samples, start=start, tune=int(num_samples / 2.0), chains=mp.cpu_count())

    varnames = ["A1", "A2", "A3", "A4", "B1", "B2", "B3", "B4"]
    pm.traceplot(trace, var_names=varnames)
    summary = az.summary(trace, var_names=varnames, credible_interval=0.95)
    print(summary)

    plt.show()

    # az.plot_hpd(x, trace["y_mean"], credible_interval=0.95)

    ppc = pm.sample_posterior_predictive(trace, samples=500, model=model)
    sample = ppc["y_pred"]

    y_fit_min = np.percentile(sample, 2.5, axis=0)
    y_fit = np.percentile(trace.y_mean, 50, axis=0)
    y_fit_max = np.percentile(sample, 97.5, axis=0)

    return y_fit, y_fit_min, y_fit_max


def run():

    # Get data
    path_to_data = "./data/processed/dd_n3he/dd_n3he_s_factor_all_data.csv"
    energy, s_factor, s_factor_error = get_processed_data(path_to_data)

    set_rcParams()
    _, ax = plt.subplots(figsize=(8, 6))
    ax.errorbar(energy, s_factor, yerr=s_factor_error,
                marker="o", color="b", elinewidth=1, linewidth=0, markersize=2, zorder=0)

    # Least-squares fit
    # coefs = lsq_fit(pade_func, energy, s_factor)
    # energy_fit = np.arange(0.8 * min(energy), 2 * max(energy), 1)
    # s_factor_fit = pade_func(energy_fit, *coefs)
    # plt.plot(energy_fit, s_factor_fit, "r-", label="lsqs")

    # Do Bayesian fitting
    y_fit, y_fit_min, y_fit_max = bayesian_fit(energy, s_factor, s_factor_error, num_samples=200)
    plt.plot(energy, y_fit, "g-", lw=2, label="PyMC3")
    plt.plot(energy, y_fit_min, "r--", lw=1)
    plt.plot(energy, y_fit_max, "r--", lw=1)

    ax.set_xlim(1, 2e4)
    ax.set_ylim(0.025, 4)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel(r"$E_{\mathrm{CM}}$ [keV]")
    ax.set_ylabel("$S$ [MeV.barn]")
    plt.legend(loc="upper left", frameon=False, fontsize=8)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    run()
