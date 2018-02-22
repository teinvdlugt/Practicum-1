from math import pi, sqrt

import numpy as np
# import matplotlib.pyplot as plt
from scipy import optimize as opt

data = np.genfromtxt("./data", delimiter=',', skip_header=1)

# Fitten met de formule:
# T = 2\pi\sqrt{L/g}

# De xdata is de lengte van het touw L. Omrekenen van cm naar m
xdata = np.take(data, [0], 1) / 100

# De ydata is de periode van de slinger T. Omrekenen van tijd van 10 slingeringen naar tijd van 1 slingering.
ydata = np.take(data, [1], 1) / 10

print(np.multiply(np.sqrt(np.divide(xdata, ydata)), 2 * pi)[:, 0])


def formula(l, g):
    return np.multiply(np.sqrt(np.divide(l, g)), 2 * pi)[:, 0]


popt, pcov = opt.curve_fit(formula, xdata, ydata)

print(popt)
print(pcov)
