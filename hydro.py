import time
import numpy as np
import math
import matplotlib.pyplot as plt
import scipy.special


def calculate_coordinates(zmin, zmax, dz):
    axis_range = np.arange(zmin, zmax, dz)
    X, Y, Z = np.meshgrid(axis_range, axis_range, axis_range)
    return X, Y, Z, axis_range


def calculate_quantum_prefactor(n, l):
    return np.sqrt((2.0 / n) ** 3 * math.factorial(n - l - 1) / (2.0 * n * math.factorial(n + l)))


def hydrogen_wf(n, l, m, X, Y, Z):
    R = np.sqrt(X ** 2 + Y ** 2 + Z ** 2)
    Theta = np.arccos(Z / R)
    Phi = np.arctan2(Y, X)

    rho = 2.0 * R / n
    s_harm = scipy.special.sph_harm(m, l, Phi, Theta)
    l_poly = scipy.special.genlaguerre(n - l - 1, 2 * l + 1)(rho)

    prefactor = calculate_quantum_prefactor(n, l)
    wf = prefactor * np.exp(-rho / 2.0) * rho ** l * s_harm * l_poly
    return np.nan_to_num(wf)


def get_sample():
    dz = 0.1
    zmin = -5
    zmax = 5

    X, Y, Z, axis_range = calculate_coordinates(zmin, zmax, dz)

    n = 1
    l = 0
    m = 0
    data = hydrogen_wf(n, l, m, X, Y, Z)
    data = np.abs(data) ** 2

    slice_idx = int(len(axis_range) / 2)
    sample = data[slice_idx, slice_idx, :]
    return list(sample)


if __name__ == "__main__":
    sample = get_sample()
    print(sample)
