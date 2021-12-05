# %%
"""https://geolite.info/geoip/v2.1/city/{ip_address}   
rq.get()
This product includes GeoLite2 data created by MaxMind, available from
<a href="https://www.maxmind.com">https://www.maxmind.com</a>."""
import numpy as np
import pandas as pd


GRID = 40
END_PUFF = 180
INTERVALS = 2
URL = 'http://forecast.weather.gov/MapClick.php?'
FIT_DICT = {'A':1,  'B':2,  'C':3,  'D':4,  'E':5,  'F':6,  'G':7}
COLORS = {'green': 1, 'yellow': 2, 'orange': 3, 'red': 4}

r_earth = 6371.0001
wind_toggle = {'m/s': 'w13u=0', 'kts': 'w13u=1', 'mph':'w13u=2', 'mis': 'w13u=3'}
lid_toggle = {0:'x100ft', 1:'x100m'}

BEARING = {'E':0,   'ESE':22.5,  'SE':45,  'SSE':67.5, 
           'S':90,  'SSW':112.5, 'SW':135, 'WSW':157.5, 
           'W':180, 'WNW':202.5, 'NW':225, 'NNW':247,  
           'N':270, 'NNE':292.5, 'NE':315, 'ENE':337.5}

FIT_ARRAY = lambda x: np.array([
    [207.473 * x ** 0.863316, np.exp(0.225596 * np.log(x) ** 2 + 2.00772 * np.log(x) + 6.04005)],
    [153.699 * x ** 0.881424, np.exp(0.0114002 * np.log(x) ** 2 + 1.05809 * np.log(x) + 4.69916)],
    [102.77 * x ** 0.8974, np.exp(-0.00192604 * np.log(x) ** 2 + 0.916609 * np.log(x) + 4.11859)],
    [67.2088 * x ** 0.902809, np.exp(-0.033014 * np.log(x) ** 2 + 0.736399 * np.log(x) + 3.4168)],
    [49.6322 * x ** 0.90287, np.exp(-0.0451795 * np.log(x) ** 2 + 0.680552 * np.log(x) + 3.05807)],
    [33.5143 * x ** 0.900409, np.exp(-0.0524468 * np.log(x) ** 2 + 0.654884 * np.log(x) + 2.61665)],
    [33.5143 * x ** 0.900409 * 2 / 3, np.exp(-0.0524468 * np.log(x) ** 2 + 0.654884 * np.log(x) + 2.61665) * 3 / 5]
])

R = lambda u: FIT_ARRAY(np.arange(-GRID, GRID + 1, u))

lambda x, y, z: np.array([(-7036 * np.exp(-0.4306 * x) + -34260.0 * np.exp(-0.009497 * x) + 58380.0 * np.exp(0.0003875 * x)) * y * 1E6 * z],
             [(1133000.0 * np.exp(0.0003455 * x) - 150400.0 * np.exp(-0.2328 * x) - 695300.0 * np.exp(-0.008704 * x)) * y * 1E6 * z],
             [(2047000.0 * np.exp(0.0004467 * x) - 257600.0 * np.exp(-0.4386 * x) - 1191000.0 * np.exp(-0.01076 * x)) * y * 1E6 * z])




def plume_conc_func(x_p, stb_class, h_lid, h_release, wind_speed):
    shape = (len(x), len(y))
    concentration = np.zeros(shape)
    disp_y = np.zeros(len(x_p))
    disp_z = np.zeros(len(x_p))
    Xbase_1 = np.zeros(len(x_p))
    Xbase_2 = np.zeros(len(x_p))
    Xbase = np.zeros(len(x_p))
    shape = (len(y), len(x_p))
    Y = np.zeros(shape)

    for i in np.arange(0, len(x_p)):
        disp_y[i] = sigma_y_func(stb_class, np.absolute(x_p[i]))
        disp_z[i] = sigma_z_func(stb_class, np.absolute(x_p[i]))
        # The base equations are needed to see which final plume equation we
        # are going to use
        Xbase_1[i] = 1 / (np.pi * disp_y[i] * disp_z[i])  # Xbase_1 is first part of equation 1
        Xbase_2[i] = 1 / (np.sqrt(2 * np.pi) * disp_y[i] * h_lid)  # Xbase_2 is equation 5

        # next if\else statement determines which base equation we will use
        if Xbase_2[i] <= Xbase_1[i]:
            Xbase[i] = Xbase_1[i] * np.exp(-.5 * (h_release / disp_z[i]) ** 2) / wind_speed / 1e6
        else:
            Xbase[i] = Xbase_2[i] / wind_speed / 1e6

        for j in np.arange(0, len(y)):
            Y[j, i] = (y[j] / disp_y[i]) ** 2  # calculates y portion of exponential function for concentration
            concentration[j, i] = Xbase[i] * np.exp(-.5 * Y[j, i])
    return concentration


##################################
# TADPUFF Concentration function #
##################################

def puff_conc_func(Xo, x_p, stb_class, h_lid, h_release):
    shape = (len(x), len(y))
    concentration = np.zeros(shape)
    disp_x = np.zeros(len(x_p))
    disp_y = np.zeros(len(x_p))
    disp_z = np.zeros(len(x_p))
    Xbase = np.zeros(len(x_p))
    shape = (len(y), len(x_p))
    Y = np.zeros(shape)
    for i in np.arange(0, len(x_p)):
        disp_x[i] = sigma_x_func(stb_class, np.absolute(x_p[i]))
        disp_y[i] = sigma_y_func(stb_class, np.absolute(x_p[i]))
        disp_z[i] = sigma_z_func(stb_class, np.absolute(x_p[i]))

        if disp_z[i] <= 1.05 * h_lid:
            Xbase[i] = 1 / (np.sqrt(2) * np.pi ** (3 / 2) * disp_x[i] * disp_y[i] * disp_z[i]) * np.exp(-.5 * ((x_p[i] - Xo) / disp_x[i]) ** 2) * np.exp(-.5 * (h_release / disp_z[i])) / 1e6
        else:
            Xbase[i] = 1 / (2 * np.pi * disp_x[i] * disp_y[i] * h_lid) * np.exp( -.5 * ((x_p[i] - Xo) / disp_y[i]) ** 2) / 1e6

        for j in np.arange(0, len(y)):
            Y[j, i] = ((y[j]) / disp_y[i]) ** 2  # calculates y portion of exponential function for concentration
            concentration[j, i] = Xbase[i] * np.exp(-.5 * Y[j, i])
    return concentration

# %%
