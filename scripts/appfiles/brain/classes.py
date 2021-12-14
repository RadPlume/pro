# %%
import numpy as np
from tkinter import *  
from tkinter import ttk

import folium
import pandas as pd
from folium import plugins
import param
tick_marks = 100                                        # This variable modifies the step interval in the grid
Intervals = 5                                           # Interval between puffs in minutes
puff_exposure = Intervals / 60;                         # puff exposure in hours
grid_length = 4e4                                       # maximum downwind distance of grid
y = np.arange(-grid_length, grid_length+1, tick_marks)  # in meters
x = np.arange(-grid_length, grid_length+1, tick_marks)  # in meters
shape = (len(x), len(y))
Xval, Yval = np.meshgrid(x, y)

# %%
fit = 6 #python starts at fit[0]
H = 50
L = 100

# equation to encompass all fits, a[0] would be Fit A and a[0 (1 is sigy 2 is sigz)]
class App(param.Parameterized):
    def __init__(self):
    
a=np.array([[207.473*x**0.863316, np.exp(0.225596*np.log(x)**2 + 2.00772*np.log(x) + 6.04005)],
            [153.699*x**0.881424, np.exp(0.0114002*np.log(x)**2 + 1.05809*np.log(x) + 4.69916)],
            [102.77*x**0.8974, np.exp(-0.00192604*np.log(x)**2 + 0.916609*np.log(x) + 4.11859)],
            [67.2088*x**0.902809, np.exp(-0.033014*np.log(x)**2 + 0.736399*np.log(x) + 3.4168)],
            [49.6322*x**0.90287, np.exp(-0.0451795*np.log(x)**2 + 0.680552*np.log(x) + 3.05807)],
            [33.5143*x**0.900409, np.exp(-0.0524468*np.log(x)**2 + 0.654884*np.log(x) + 2.61665)],
            [(33.5143*x**0.900409)*2/3, np.exp(-0.0524468*np.log(x)**2 + 0.654884*np.log(x) + 2.61665)*3/5]])




sigy = a[fit,0]
sigz = a[fit,1]

r =  1 / (L * np.sqrt(2*np.pi) * sigy)
k = 1 / (np.pi * sigy * sigz) 

k2 = lambda x: k * np.exp(-0.5*(H/x)**2)

ch = np.where(r<=k,k2(sigz),r)
# good to here   
# %%
