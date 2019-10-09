"""
----------------------
dd_n3he_s_factor_fitting
----------------------

Script to use Bayesian linear regression to fit the S-factor data for the d + d --> n + 3He

:Date: 06/08/2019
"""

import matplotlib.pyplot as plt
import numpy as np
import pymc3 as pm
import arviz as az
import pandas as pd
import multiprocessing as mp
from scipy.optimize import curve_fit


def get_data(path_to_file):
    data = pd.read_csv(path_to_file, header=0, delimiter=",")
    energy = np.array(data.iloc[:, 0].values)
    s_factor = np.array(data.iloc[:, 1].values)
    s_factor_error = np.array(data.iloc[:, 2].values)
    return energy, s_factor, s_factor_error


# def do_lsq_fit(x, y, y_error):
#
#     coefs, _ = curve_fit(pade_func, x, y, sigma=y_error, absolute_sigma=True)
#     x_fit = np.logspace(-1, 6, 1000)
#     y_fit = pade_func(x_fit, coefs[0], coefs[1], coefs[2], coefs[3], coefs[4])
#
#     return x_fit, y_fit


def do_bayesian_fit(x, y, y_error, num_samples=500):

    def pade_func(x_array, A1, A2, A3, A4):
        return A1 + x_array * (A2 + x_array * (A3 + x_array * A4))

    with pm.Model() as model:

        # Setup the model
        A1 = pm.Flat("A1")
        A2 = pm.Flat("A2")
        A3 = pm.Flat("A3")
        A4 = pm.Flat("A4")
        y_stdev = pm.HalfNormal("Y_stdev", sd=1)

        y_mean = pm.Deterministic("y_mean", pade_func(x, A1, A2, A3, A4))
        # y_pred = pm.Normal("y_pred", mu=y_mean, observed=y)
        y_pred = pm.Normal("y_pred", mu=y_mean, sd=y_stdev, observed=y)
        # y_pred = pm.Normal("y_pred", mu=y_mean, tau=1.0/y_error**2, observed=y)

        # Do the fitting
        start = pm.find_MAP()
        trace = pm.sample(num_samples, start=start, tune=int(num_samples / 2.0), chains=mp.cpu_count())

    varnames = ["A1", "A2", "A3", "A4"]
    pm.traceplot(trace, var_names=varnames)
    summary = az.summary(trace, var_names=varnames, credible_interval=0.95)
    print(summary)

    plt.show()

    # az.plot_hpd(x, trace["y_mean"], credible_interval=0.95)

    ppc = pm.sample_posterior_predictive(trace, samples=200, model=model)
    sample = ppc["y_pred"]

    y_fit_min = np.percentile(sample, 2.5, axis=0)
    y_fit = np.percentile(trace.y_mean, 50, axis=0)
    y_fit_max = np.percentile(sample, 97.5, axis=0)

    return y_fit, y_fit_min, y_fit_max


def run():

    # Get data
    path_to_data = "/Users/pallan/Documents/dd_cross_section_work/data/dd_n3he/dd_n3he_s_factor_all_data.csv"
    energy, s_factor, s_factor_error = get_data(path_to_data)

    # Do Bayesian fitting
    y_fit, y_fit_min, y_fit_max = do_bayesian_fit(energy, s_factor, s_factor_error, num_samples=2000)
    plt.plot(energy, y_fit, "r-", lw=2)
    plt.plot(energy, y_fit_min, "r--", lw=2)
    plt.plot(energy, y_fit_max, "r--", lw=2)

    # x_fit, y_fit = do_lsq_fit(energy, s_factor, s_factor_error)
    # plt.plot(x_fit, y_fit)

    plt.errorbar(energy, s_factor, yerr=s_factor_error, marker="o", color="b", elinewidth=1, linewidth=0,
                 markersize=0.5)

    plt.xlim(1, 1e4)
    plt.ylim(0.02, 1)
    plt.xscale("log")
    plt.yscale("log")
    plt.show()


if __name__ == "__main__":
    run()
