from math import pi, sqrt

import numpy as np
# import matplotlib.pyplot as plt
from scipy import optimize as opt

data = np.genfromtxt("./data.csv", delimiter=',', skip_header=1)

# Fitten met de formule:
# T = 2\pi\sqrt{L/g}

# De xdata is de lengte van het touw L. Omrekenen van cm naar m
xdata = np.take(data, [0], 1) / 100
# Fout in x:
xerr = np.take(data, [2], 1) / 100

# De ydata is de periode van de slinger T. Omrekenen van tijd van 10 slingeringen naar tijd van 1 slingering.
ydata = np.take(data, [1], 1) / 10
# De yerr is de fout in T gedeeld door 10
yerr = np.take(data, [3], 1) / 10

print(np.multiply(np.sqrt(np.divide(xdata, ydata)), 2 * pi)[:, 0])


def formula(l, g):
    return np.multiply(np.sqrt(np.divide(l, g)), 2 * pi)


popt, pcov = opt.curve_fit(formula, xdata.ravel(), ydata.ravel(), sigma=yerr.ravel(),
                           absolute_sigma=True)

print(popt)
print(pcov)

""" Nu met ODR -- https://docs.scipy.org/doc/scipy/reference/odr.html """
print("====== ODR =======")
from scipy import odr, power
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker


def formula(B, x):
    # Function: 2*pi*sqrt(x/B[0])
    # B is a vector of the parameters. -- in our case [g]
    # x is an array of the current x values.
    # x is in the same format as the x passed to Data or RealData.
    #
    # Return an array in the same format as y passed to Data or RealData.
    return 2 * pi * np.sqrt(x / B[0])


# Instantiate
model = odr.Model(formula)
data = odr.Data(xdata, ydata, wd=1. / power(xerr, 2), we=1. / power(yerr, 2))  # weight = 1/(S_g^2)
odr_instance = odr.ODR(data, model, beta0=[9.81])  # Initial estimate: g = 9.81

# Run the fit
output = odr_instance.run()
output.pprint()  # Prints summary of results

# Plot results
# First plot measured data points:
# plt.plot(xdata, ydata, 'ro')
plt.errorbar(xdata, ydata, yerr, xerr, 'ro', elinewidth=.5, markersize=4, capsize=1)

# Plot fitted curve
x = np.linspace(1, 2, 100)
y = formula(output.beta, x)
plt.plot(x, y, label='ODR approximation\n g=%f ± %f' % (output.beta, output.sd_beta))
# Show plots
plt.title('Slingerproef')
plt.xlabel('Lengte slinger L (m)')
plt.ylabel('Periode T (s)')
plt.legend()
plt.grid()
plt.show()
