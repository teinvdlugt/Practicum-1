import numpy as np
import matplotlib.pyplot as plt
from scipy import odr, power
from math import sqrt

# Determine the I-to-B factor:
B_per_I = 0.0007792861142  # Zie opdracht in labdagboek

# Fetch data
data = np.genfromtxt("data.csv", delimiter=',', skip_header=1)

U_data = np.take(data, [0], 1).ravel()  # In volts
I_data = np.take(data, [1], 1).ravel()  # In amperes
B_data = B_per_I * I_data  # Calculate magnetic field strength B from current I
x_data = np.array([U_data, B_data])  # Combine inputs
y_data = np.take(data, [2], 1).ravel() / 2000  # Radius, from diameter in mm to radius in m

U_err = np.take(data, [3], 1).ravel()           # In volts
I_err = np.take(data, [4], 1).ravel()           # In amperes
# B_err = # TODO combine 2 errors               # Calculate magnetic field strength B from current I
x_err = np.array([U_data, B_data])              # Combine inputs
y_err = np.take(data, [5], 1).ravel() / 2000    # Radius, from diameter in mm to radius in m


def formula(B, x):
    """ B is the vector with values to be fitted: B[0] = e/m.
    x is the array of inputs, of shape (2, n), where n is the number
    of observations. The first row is voltage U (V), the second row is
    magnetic field strength B (T). Returns the calculated radius of the cathode ray.
    Fit to the formula:
    e/m = 2U/r^2B^2 \Rightarrow r = \sqrt{2U/CB^2}, with C = e/m = B[0]
    """
    return np.sqrt(2 * x[0] / (B[0] * np.square(x[1])))


model = odr.Model(formula)
data = odr.Data(x_data, y_data)  # wd=1. / power(xerr, 2), we=1. / power(yerr, 2)""")  # weight = 1/(S_g^2)
odr_instance = odr.ODR(data, model, beta0=[1.76e11])  # Initial estimate: e/m = 1.76e11

# Run the fit
output = odr_instance.run()
output.pprint()  # Prints summary of results
