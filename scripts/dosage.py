'''Handles the calculations for RadPlume'''
import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import warnings

ui = GUI()
warnings.filterwarnings("ignore")  # turn off iteration warnings




class Dose(ui):
    def __init_subclass__(cls) -> None:
        return super().__init_subclass__()

    def iodines(self, tedi, adult, child):
        tedi = (-7036 * np.exp(-.4306 * holdup) + (-3.426e4) * np.exp(-.009497 * holdup) + 5.838e4 * np.exp(
            3.875e-4 * holdup)) * iodine_rate * (100 ** 3) * exposure
        adult = (1.133e6 * np.exp((3.455e-4) * holdup) - 1.504e5 * np.exp(-.2328 * holdup) - 6.953e5 * np.exp(
            -.008704 * holdup)) * iodine_rate * (100 ** 3) * exposure
        child = (2.047e6 * np.exp(4.467e-4 * holdup) - 2.576e5 * np.exp(-.4386 * holdup) - 1.191e6 * np.exp(
            -.01076 * holdup)) * iodine_rate * (100 ** 3) * exposure
        return tedi, adult, child

    def particulates(self, tedp):
        tedp = 4.3e4 * self.partic_rate * (100 ** 3) * self.exposure
        return tedp

    def nobles(dose, tedn):
        
        if holdup == 0:
            l_holdup = 0
        else:
            l_holdup = np.log(self.holdup)

        if exposure == 0:
            l_exposure = 0
        else:
            l_exposure = np.log(self.exposure)

        # coefficients
        p00 = 287.1
        p10 = -39.3
        p01 = -73.16
        p20 = -10.36
        p11 = 22.67
        p02 = -17.52
        p30 = -0.5556
        p21 = 4.307
        p12 = -4.229
        p03 = 6.866
        p31 = 0.0811
        p22 = -0.4185
        p13 = 0.2565
        p04 = -0.5276

        tedn = (p00 + p10 * l_exposure + p01 * l_holdup + p20 * l_exposure ** 2 + p11 * l_exposure * l_holdup + p02 * l_holdup ** 2 + p30 * l_exposure ** 3 + p21 * l_exposure ** 2 * l_holdup + p12 * l_exposure * l_holdup ** 2 + p03 * l_holdup ** 3 + p31 * l_exposure ** 3 * l_holdup
                + p22 * l_exposure ** 2 * l_holdup ** 2 + p13 * l_exposure * l_holdup ** 3 + p04 * l_holdup ** 4) * noble_rate * (100 ** 3) * exposure
        return tedn

