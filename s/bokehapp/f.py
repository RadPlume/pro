# %%
######################################################################
# Radioactive Plume Equations ver. 3                                 #
# By Mitch Gatewood                                                  #                           
# input variables needed                                             #
# ui.p_mu, class (stability), ui.p_ht (release height)          #
# ui.p_lid (mixing lid), ui.p_tdel (ui.p_tdel time), ui.p_hup (ui.p_hup time) #
######################################################################
import folium
import numpy as np 
import panel as pn
import pandas as pd
import matplotlib.pyplot as plt
from folium.plugins import HeatMap
from folium import plugins
from panel import widgets
from mpl_toolkits import mplot3d
import warnings
import tkinter as tk                     # the GUI package we'll be using
import tkinter
from ui import GUI
from dose import Dose


pn.extension()
dose = Dose()

ui = GUI()
warnings.filterwarnings("ignore")  # turn off iteration warnings
ui.p_tick = 5  # This variable modifies the step interval in the grid
Intervals = 2  # Interval between puffs in minutes
End_puff = 12*15  # how many puffs are to be calculated
grid_length = 40  # maximum downwind distance of grid
y = np.arange(-grid_length * 1000, grid_length * 1001, ui.p_tick * 100)  # in meters
x = np.arange(-grid_length, grid_length + ui.p_tick / 10, ui.p_tick / 10)  # in kilometers
shape = (len(x), len(y))
Xval, Yval = np.meshgrid(x, y)

# Concentration variables

ted_total = np.zeros(shape)
ted_puff = np.zeros(shape)
adult_total = np.zeros(shape)
child_total = np.zeros(shape)

################################################################
# puff tracking array                                          #
#                                                              #
# This matrix is used to keep track of each puff in the system #
# Column 1 is the puff number, Column 2 is the puff index      #
# Column 3 is the stability classs, Column 4 is wind speed     #
# Column 5 is the wind direction                               #
################################################################

shape = (End_puff, End_puff, 3)
puff_track = np.zeros(shape)

##############################
# Reactor Release Parameters #
##############################

ui.p_hup = 0.5
ui.p_tdel = 3
ui.p_iodine = 10
ui.p_noble = 200
ui.p_partic = 1
ui.p_ht = 10
ui.p_mu = 1.788

##############################
# Atmospheric Conditions     #
##############################

# fit selects which stability class to plot, A-F are 1-5 respectively
fit = 3
ui.p_lid = 800

# SIGMA_Y_COEF are the coefficients for the sigma y stablilty classes
SIGMA_Y_COEF = np.array([[207.473, .863316],
                         [153.669, .881424],
                         [102.77, .8974],
                         [67.2088, .902809],
                         [49.6322, .902878],
                         [33.5143, .900409]])
# SIGMA_Z_COEF are the coefficients for the sigma Z stablilty classes
SIGMA_Z_COEF = np.array([[.225596, 2.00772, 6.04005],
                         [.0114002, 1.05809, 4.69916],
                         [-.00192604, .916609, 4.11859],
                         [-.033014, .736399, 3.4168],
                         [-.0451795, .680552, 3.05807],
                         [-.0524468, .654884, 2.61665]])


#########################################################
# sigma_y function is used to calculate the sigma y fit #
# x = location in x direction                           #
# class = stability class                               #
#########################################################
def sigma_y_func(fit, x):
    if fit < 6:
        sigma_y = SIGMA_Y_COEF[int(fit), 0] * x ** (SIGMA_Y_COEF[int(fit), 1])
    else:
        sigma_y = 2 / 3 * (SIGMA_Y_COEF[5, 0] * x ** (SIGMA_Y_COEF[5, 1]))
    return sigma_y


#########################################################
# sigma_x function is used to calculate the sigma y fit #
# x = location in x direction                           #
# class = stability class                               #
#########################################################
def sigma_x_func(fit, x):
    if fit < 6:
        sigma_x = SIGMA_Y_COEF[int(fit), 0] * x ** (SIGMA_Y_COEF[int(fit), 1])
    else:
        sigma_x = 2 / 3 * (SIGMA_Y_COEF[5, 0] * x ** (SIGMA_Y_COEF[5, 1]))
    return sigma_x


#########################################################
# sigma_z function is used to calculate the sigma z fit #
# x = location in x direction                           #
# class = stability class                               #
#########################################################
def sigma_z_func(fit, x):

    if fit < 6:
        sigma_z = np.exp(
            SIGMA_Z_COEF[int(fit), 0] * (np.log(x)) ** 2 + SIGMA_Z_COEF[int(fit), 1] * np.log(x) +
            SIGMA_Z_COEF[int(fit), 2])
    else:
        sigma_z = 2 / 3 * (
            np.exp(SIGMA_Z_COEF[5, 0] * (np.log(x)) ** 2 + SIGMA_Z_COEF[5, 1] * np.log(x) + SIGMA_Z_COEF[5, 2]))
    return sigma_z


########################################################
# Iodines fit function                                 #
# these fit equations were created using MATLAB cftool #
# ui.p_hup = ui.p_hup time                                 #
# ui.p_tdel = ui.p_tdel time                             #
# ui.p_iodine = Iodines release rate                   #
# tedi= TED dose                                       #
# adult = adult dose                                   #
# child = child dose                                   #
########################################################

def iodines_func(ui):
    tedi = (-7036 * np.exp(-.4306 * ui.p_hup) + (-3.426e4) * np.exp(-.009497 * ui.p_hup) + 5.838e4 * np.exp(
        3.875e-4 * ui.p_hup)) * ui.p_iodine * (100 ** 3) * ui.p_tdel
    adult = (1.133e6 * np.exp((3.455e-4) * ui.p_hup) - 1.504e5 * np.exp(-.2328 * ui.p_hup) - 6.953e5 * np.exp(
        -.008704 * ui.p_hup)) * ui.p_iodine * (100 ** 3) * ui.p_tdel
    child = (2.047e6 * np.exp(4.467e-4 * ui.p_hup) - 2.576e5 * np.exp(-.4386 * ui.p_hup) - 1.191e6 * np.exp(
        -.01076 * ui.p_hup)) * ui.p_iodine * (100 ** 3) * ui.p_tdel
    return tedi, adult, child


########################################################
# Nobles fit function                                  #
# these fit equations were created using MATLAB cftool #
# ui.p_noble = Noble release rate                      #
# ui.p_hup = ui.p_hup time                                 #
# ui.p_tdel = ui.p_tdel time                             #
# tedn= TED dose                                       #
########################################################

def nobles(ui):
    if ui.p_hup == 0:
        l_holdup = 0
    else:
        l_holdup = np.log(ui.p_hup)

    if ui.p_tdel == 0:
        l_exposure = 0
    else:
        l_exposure = np.log(ui.p_tdel)

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
            + p22 * l_exposure ** 2 * l_holdup ** 2 + p13 * l_exposure * l_holdup ** 3 + p04 * l_holdup ** 4) * ui.p_noble * (100 ** 3) * ui.p_tdel
    return tedn


########################################################
# Cesiums function                                     #
# ui.p_tdel = ui.p_tdel time                             #
# ui.p_partic = Cesiums release rate                   #
# tedp= TED dose                                       #
########################################################

def particulates(ui):
    tedp = 4.3e4 * ui.p_partic * (100 ** 3) * ui.p_tdel
    return tedp




#############################################################
# x Calculation Function                                    #
#                                                           #
# This function is to provide the dispersion x values       #
# Inputs:                                                   #
# wind speed                                                #
# num_moved is how many times current puff has moved        #
# distance                                                  #
# size of the grid                                          #
#############################################################

def x_calc(grid_length, num_moved, ui, distance):
    x_index_start = 0
    x_index_end = 0
    x_puff = np.zeros(len(x))
    puff_length = round(ui.p_mu * Intervals * (num_moved + 1) * 60 / 1000, 1)

    if distance <= grid_length:  # has puff gone outside of the grid?
        x_index_start = int(round((40 + distance - puff_length / 2) / (ui.p_tick * .1), 1))  # calculate puff start index
    else:
        x_puff = np.zeros(1, len(x))  # it has so nothing to calculate

    if distance + puff_length / 2 > grid_length:  # is the end of the puff outside of the grid?
        x_index_end = len(x_puff)  # if so then we calculate only to the end of the grid
    else:
        x_index_end = int(round(40 + distance + puff_length / 2, 1) / (ui.p_tick * .1) + 1)  # calculate the end

    if x_index_start != 0:  # if the puff starts inside of the grid
        x_puff[x_index_start: x_index_end] = x[x_index_start:x_index_end]  # calculate puff parameters
    return x_puff


###################################
# TADPLUME Concentration function #
###################################

def plume_conc_func(x_p, fit, ui):
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
        disp_y[i] = sigma_y_func(fit, np.absolute(x_p[i]))
        disp_z[i] = sigma_z_func(fit, np.absolute(x_p[i]))
        # The base equations are needed to see which final plume equation we
        # are going to use
        Xbase_1[i] = 1 / (np.pi * disp_y[i] * disp_z[i])  # Xbase_1 is first part of equation 1
        Xbase_2[i] = 1 / (np.sqrt(2 * np.pi) * disp_y[i] * ui.p_lid)  # Xbase_2 is equation 5

        # next if\else statement determines which base equation we will use
        if Xbase_2[i] <= Xbase_1[i]:
            Xbase[i] = Xbase_1[i] * np.exp(-.5 * (ui.p_ht / disp_z[i]) ** 2) / ui.p_mu / 1e6
        else:
            Xbase[i] = Xbase_2[i] / ui.p_mu / 1e6

        for j in np.arange(0, len(y)):
            Y[j, i] = (y[j] / disp_y[i]) ** 2  # calculates y portion of exponential function for concentration
            concentration[j, i] = Xbase[i] * np.exp(-.5 * Y[j, i])
    return concentration


##################################
# TADPUFF Concentration function #
##################################

def puff_conc_func(Xo, x_p, fit, ui):
    shape = (len(x), len(y))
    concentration = np.zeros(shape)
    disp_x = np.zeros(len(x_p))
    disp_y = np.zeros(len(x_p))
    disp_z = np.zeros(len(x_p))
    Xbase = np.zeros(len(x_p))
    shape = (len(y), len(x_p))
    Y = np.zeros(shape)
    for i in np.arange(0, len(x_p)):
        disp_x[i] = sigma_x_func(fit, np.absolute(x_p[i]))
        disp_y[i] = sigma_y_func(fit, np.absolute(x_p[i]))
        disp_z[i] = sigma_z_func(fit, np.absolute(x_p[i]))

        if disp_z[i] <= 1.05 * ui.p_lid:
            Xbase[i] = 1 / (np.sqrt(2) * np.pi ** (3 / 2) * disp_x[i] * disp_y[i] * disp_z[i]) * np.exp(-.5 * ((x_p[i] - Xo) / disp_x[i]) ** 2) * np.exp(-.5 * (ui.p_ht / disp_z[i])) / 1e6
        else:
            Xbase[i] = 1 / (2 * np.pi * disp_x[i] * disp_y[i] * ui.p_lid) * np.exp( -.5 * ((x_p[i] - Xo) / disp_y[i]) ** 2) / 1e6

        for j in np.arange(0, len(y)):
            Y[j, i] = ((y[j]) / disp_y[i]) ** 2  # calculates y portion of exponential function for concentration
            concentration[j, i] = Xbase[i] * np.exp(-.5 * Y[j, i])
    return concentration


#######################
# Main Body of Script #
#######################

###########################################
# Generate the puffs.                     #
# right now they all have same wind speed #
# stability classes                       #
###########################################

for puff_num in range(End_puff):
    for num_moved in range(End_puff - puff_num):
        puff_track[puff_num, num_moved, 0] = fit
        puff_track[puff_num, num_moved, 1] = ui.p_mu
        puff_track[puff_num, num_moved, 2] = 1  # direction for future use

########################################
# Calculate concentration of each puff #
# Then add them together in order to   #
# total the concentration              #
########################################

for puff_num in range(End_puff):
    puff_distance = 0
    num_moved = 0

    # for loop calculates distance the puff has traveled
    for num_moved in range(End_puff - puff_num - 1):
        puff_distance = puff_distance + puff_track[puff_num, num_moved, 1] * Intervals * 60 / 1000  # how far will puff move

    puff_distance = round(puff_distance, 1)
    fit = puff_track[puff_num, num_moved, 0]  # get the current stability class for the puff
    ui.p_mu = puff_track[puff_num, num_moved, 1]  # get the current wind speed of the puff

    # get the puff\plume distance\length parameters
    x_puff = x_calc(grid_length, num_moved, ui.p_mu, puff_distance)

    # get the dispersion of the puff\plume
    if puff_num == End_puff - 1:
        concentration = plume_conc_func(x_puff, fit, ui)  # calculate the concentration using plume
    else:
        concentration = puff_conc_func(puff_distance, x_puff, fit, ui)  # calculate the concentration

    dose.iodines()
    dose.

    # calculate the TED puff concentrations
    ted_puff = (tedi + tedn + tedp) * concentration
    ted_puff[np.isnan(ted_puff)] = 0  # get rid of any NaN values
    ted_total = ted_total + ted_puff

    # calculate the Adult puff concentrations
    adult_puff = adult_dose * concentration
    adult_puff[np.isnan(adult_puff)] = 0  # get rid of any NaN values
    adult_total = adult_total + adult_puff

    # calculate the child puff concentrations
    child_puff = child_dose * concentration
    child_puff[np.isnan(child_puff)] = 0  # get rid of any NaN values
    child_total = child_total + child_puff

# Plots

fig = plt.figure()
plt.contourf(Xval, Yval / 1000, ted_total * 1000, levels=[10, 100, 1000, 5000],
             colors=['#00CD00', 'yellow', 'orange', 'red'], extend='max')
plt.ylim(-3, 3)
plt.xlim(0, 40)
plt.title('TED Dose')
plt.xlabel('Downwind Distance (kilometers)')
plt.ylabel('Off-center distance (kilomethers)')
plt.show()

#fig = plt.figure()
plt.contourf(Xval, Yval / 1000, adult_total, levels=[1, 5, 10, 500], colors=['#00CD00', 'yellow', 'orange', 'red'],
             extend='max')
plt.ylim(-3, 3)
plt.xlim(0, 40)
plt.title('Adult Dose')
plt.xlabel('Downwind Distance (kilometers)')
plt.ylabel('Off-center distance (kilomethers)')
plt.show()

#fig = plt.figure()
plt.contourf(Xval, Yval / 1000, child_total, levels=[1, 5, 10, 500], colors=['#00CD00', 'yellow', 'orange', 'red'],
             extend='max')
plt.ylim(-3, 3)
plt.xlim(0, 40)
plt.title('Child Dose')
plt.xlabel('Downwind Distance (kilometers)')
plt.ylabel('Off-center distance (kilomethers)')
plt.show()

# After the plant is selected from the dropdown, lat1 and long1 need to be
# updated to refelect the selected plant. 

# map starting location Palo Verde Unit 2
lat1 = 33.38737234
long1 = -112.8653472

# After running the dose equation, the Y values need to be converted into km
newY = Yval /1000

############### Convert X and Y into lat and long coordinates #############

# radius of earth (km)
r_earth = 6371.0001

# Get direction input and choose angle from pre-defined list or have user input variable



### if direction = E, then angle = 0
### if direction = SE, then angle = 45
### if direction = S, then angle = 90
### if direction = SW, then angle = 135
### if direction = W, then angle = 180
### if direction = NW, then angle = 225
### if direction = N, then angle = 270
### if direction = NE, then angle = 315


#alpha = (angle * (np.pi/180))
alpha = (0 * (np.pi/180))

## position rotation formula
X_1 = (Xval*np.cos(alpha)) + (newY*np.sin(alpha))

Y_1 = (newY*np.cos(alpha)) - (Xval*np.sin(alpha))

#Latitude from X
for element in Y_1:
    lats = lat1 + (Y_1/r_earth)*(180/np.pi)

#Longitude from Y
for element in X_1:
    longs = long1 + (X_1/r_earth) * ((180/np.pi) / np.cos(lat1 * np.pi/180))
    
###############lats1, longs1, and dose need to be flattened ################
    
# lat coordinates from Xval
lats1 = (np.asarray(lats)).flatten()


# long coordinates from Yval
longs1 = (np.asarray(longs)).flatten()

# dose data
dose = (np.asarray(ted_total)).flatten()


############### TED Dose Area #############

# check for values greater than 5 rem in dose data
red = np.where(dose > 5)

# make new lats list with index list corresponding to 5 rem dose data values
for las in lats1:
    lats2 = lats1[red]
    
# make new longs list with index list corresponding to 5 rem dose data values
for lon in longs1:
    longs2 = longs1[red]   
 
# make new red dose list to be used for pandas dataframe    
for rdose in dose:
    red_dose = dose[red]

# red area pandas df to iterate folium circles function with
red_area = pd.DataFrame({
    'lats': lats2,
    'lons': longs2,
    'dose': red_dose
})


# check for values less than or equal to 5 rem and greater than 1 rem in dose data
orange = np.where((dose <= 5) & (dose > 1))

# make new lats list with index list corresponding to orange dose data values
for lass in lats1:
    lats3 = lats1[orange]

# make new longs list with index list corresponding to orange dose data values
for lonn in longs1:
    longs3 = longs1[orange]   

# make new orange dose list to be used for pandas dataframe    
for odose in dose:
    orange_dose = dose[orange]

# pandas data fram with orange data    
orange_area = pd.DataFrame({
    'lats1': lats3,
    'lons1': longs3,
    'dose': orange_dose
})

# check for values less than or equal to 1 rem and greater than 0.1 rem in dose data
yellow = np.where((dose <= 1) & (dose > 0.1))

# make new lats list with index list corresponding to yellow dose data values
for lasss in lats1:
    lats4 = lats1[yellow]

# make new longs list with index list corresponding to yellow dose data values
for lonnn in longs1:
    longs4 = longs1[yellow]

# make new yellow dose list to be used for pandas dataframe    
for ydose in dose:
    yellow_dose = dose[yellow] 
 
# pandas data fram with yellow data    
yellow_area = pd.DataFrame({
    'lats2': lats4,
    'lons2': longs4,
    'dose': yellow_dose
})

# check for values less than 0.1 rem (100 millirem) and greater than 0.001 rem (1000 millirem) in dose data
green = np.where((dose <= 0.1) & (dose > 0.001))

# make new lats list with index list corresponding to green dose data values
for lassss in lats1:
    lats5 = lats1[green]

# make new longs list with index list corresponding to green dose data values
for lonnnn in longs1:
    longs5 = longs1[green]
    
# make new green dose list to be used for pandas dataframe    
for gdose in dose:
    green_dose = dose[green] 

# pandas data fram with green data    
green_area = pd.DataFrame({
    'lats3': lats5,
    'lons3': longs5,
    'dose': green_dose
})


####################Creating the map##############

#To create map, location should be [lat1,long1]
Rad_Map = folium.Map(
    location=[33.38749636791151, -112.86533282010271],
    zoom_start=10
)



#Add dose area layers to map
FG_TED = folium.FeatureGroup(name="TED Dose").add_to(Rad_Map)
FG_Adult = folium.FeatureGroup(name="Adult Thyroid Dose", show=False).add_to(Rad_Map)
FG_Child = folium.FeatureGroup(name="Child Thyroid Dose", show=False).add_to(Rad_Map)
FG_EM = folium.FeatureGroup(name="EM Worker Dose", show=False).add_to(Rad_Map)



#Add Layer Control
folium.LayerControl().add_to(Rad_Map)

#Add measure tool 
plugins.MeasureControl(position='topright', primary_length_unit='meters', secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(Rad_Map)

#################### Adding the TED colored circles to the map ##############

# add red marker one by one on the map
for i in range(0,len(red_area)):
    FG_TED.add_child(folium.Circle(
      location=[red_area.iloc[i]['lats'], red_area.iloc[i]['lons']],
      popup=red_area.iloc[i]['dose'],
      radius=50,
      color="red",
      fill=True,
      fill_color="red"
   ))
    
# add orange marker one by one on the map
for i in range(0,len(orange_area)):
    FG_TED.add_child(folium.Circle(
      location=[orange_area.iloc[i]['lats1'], orange_area.iloc[i]['lons1']],
      popup=orange_area.iloc[i]['dose'],
      radius=50,
      color="orange",
      fill=True,
      fill_color="orange"
   ))

# add yellow marker one by one on the map
for i in range(0,len(yellow_area)):
    FG_TED.add_child(folium.Circle(
      location=[yellow_area.iloc[i]['lats2'], yellow_area.iloc[i]['lons2']],
      popup=yellow_area.iloc[i]['dose'],
      radius=50,
      color="yellow",
      fill=True,
      fill_color="yellow"
   ))

# add green marker one by one on the map
for i in range(0,len(green_area)):
    FG_TED.add_child(folium.Circle(
      location=[green_area.iloc[i]['lats3'], green_area.iloc[i]['lons3']],
      popup=green_area.iloc[i]['dose'],
      radius=50,
      color="green",
      fill=True,
      fill_color="green"
   ))
    
############### Adult Thyroid Dose Area #############

# dose data updates
dose1 = (np.asarray(adult_total)).flatten()

# check for values greater than or equal to 500 rem in dose data
red1 = np.where(dose1 >= 500)

# make new lats list with index list corresponding to 5 rem dose data values
for las in lats1:
    lats6 = lats1[red1]
    
# make new longs list with index list corresponding to 5 rem dose data values
for lon in longs1:
    longs6 = longs1[red1]   
 
# make new red dose list to be used for pandas dataframe    
for rdose in dose1:
    red_dose1 = dose1[red1]
    
# red area pandas df to iterate folium circles function with
red_area1 = pd.DataFrame({
    'lats': lats6,
    'lons': longs6,
    'dose': red_dose1
})

# check for values less than 500 rem and greater than or equal to 10 rem in dose data
orange1 = np.where((dose1 < 500) & (dose1 >= 10))

# make new lats list with index list corresponding to orange dose data values
for lass in lats1:
    lats7 = lats1[orange1]

# make new longs list with index list corresponding to orange dose data values
for lonn in longs1:
    longs7 = longs1[orange1]   
    
# make new orange dose list to be used for pandas dataframe        
for odose in dose1:
    orange_dose1 = dose1[orange1]

# pandas data fram with orange data    
orange_area1 = pd.DataFrame({
    'lats1': lats7,
    'lons1': longs7,
    'dose': orange_dose1
})

# check for values less than to 10 rem and greater than or equal to 5 rem in dose data
yellow1 = np.where((dose1 < 10) & (dose1 >= 5))

# make new lats list with index list corresponding to yellow dose data values
for lasss in lats1:
    lats8 = lats1[yellow1]

# make new longs list with index list corresponding to yellow dose data values
for lonnn in longs1:
    longs8 = longs1[yellow1]

# make new yellow dose list to be used for pandas dataframe    
for ydose in dose1:
    yellow_dose1 = dose1[yellow1] 
 
# pandas data fram with yellow data    
yellow_area1 = pd.DataFrame({
    'lats2': lats8,
    'lons2': longs8,
    'dose': yellow_dose1
})

# check for values less than 0.1 rem (100 millirem) and greater than 0.001 rem (1000 millirem) in dose data
green1 = np.where((dose1 < 5) & (dose1 > 0.1))

# make new lats list with index list corresponding to green dose data values
for lassss in lats1:
    lats9 = lats1[green1]

# make new longs list with index list corresponding to green dose data values
for lonnnn in longs1:
    longs9 = longs1[green1]
    
# make new green dose list to be used for pandas dataframe    
for gdose in dose1:
    green_dose1 = dose1[green1] 

# pandas data fram with green data    
green_area1 = pd.DataFrame({
    'lats3': lats9,
    'lons3': longs9,
    'dose': green_dose1
})


#################### Adding the Adut Thyroid colored circles to the map ##############

# add marker one by one on the map
for i in range(0,len(red_area1)):
    FG_Adult.add_child(folium.Circle(
      location=[red_area1.iloc[i]['lats'], red_area1.iloc[i]['lons']],
      popup=red_area1.iloc[i]['dose'],
      radius=50,
      color="red",
      fill=True,
      fill_color="red"
   ))
    
# add marker one by one on the map
for i in range(0,len(orange_area1)):
    FG_Adult.add_child(folium.Circle(
      location=[orange_area1.iloc[i]['lats1'], orange_area1.iloc[i]['lons1']],
      popup=orange_area1.iloc[i]['dose'],
      radius=50,
      color="orange",
      fill=True,
      fill_color="orange"
   ))

# add marker one by one on the map
for i in range(0,len(yellow_area1)):
    FG_Adult.add_child(folium.Circle(
      location=[yellow_area1.iloc[i]['lats2'], yellow_area1.iloc[i]['lons2']],
      popup=yellow_area1.iloc[i]['dose'],
      radius=50,
      color="yellow",
      fill=True,
      fill_color="yellow"
   ))
    
# add marker one by one on the map
for i in range(0,len(green_area1)):
    FG_Adult.add_child(folium.Circle(
      location=[green_area1.iloc[i]['lats3'], green_area1.iloc[i]['lons3']],
      popup=green_area1.iloc[i]['dose'],
      radius=50,
      color="green",
      fill=True,
      fill_color="green"
   ))
    
    
############### Child Thyroid Dose Area #############

# dose data update
dose2 = (np.asarray(child_total)).flatten()

# check for values greater than or equal to 500 rem in dose data
red2 = np.where(dose2 >= 500)

# make new lats list with index list corresponding to 5 rem dose data values
for las in lats1:
    lats10 = lats1[red2]
    
# make new longs list with index list corresponding to 5 rem dose data values
for lon in longs1:
    longs10 = longs1[red2]    

# make new red dose list to be used for pandas dataframe       
for rdose in dose2:
    red_dose2 = dose2[red2]

# make new red dose list to be used for pandas dataframe        
red_area2 = pd.DataFrame({
    'lats': lats10,
    'lons': longs10,
    'dose': red_dose2
})
  
# check for values less than 500 rem and greater than or equal to 100 rem in dose data
orange2 = np.where((dose2 < 500) & (dose2 >= 5))
    
# make new lats list with index list corresponding to orange dose data values
for lass in lats1:
    lats11 = lats1[orange2]

# make new longs list with index list corresponding to orange dose data values
for lonn in longs1:
    longs11 = longs1[orange2]   
    
# make new orange dose list to be used for pandas dataframe        
for odose in dose2:
    orange_dose2 = dose2[orange2]

# pandas data fram with orange data    
orange_area2 = pd.DataFrame({
    'lats1': lats11,
    'lons1': longs11,
    'dose': orange_dose2
})  
    
# check for values less than 5 rem and greater than or equal to 1 rem in dose data
yellow2 = np.where((dose2 < 5) & (dose2 >= 1))
    
# make new lats list with index list corresponding to yellow dose data values
for lasss in lats1:
    lats12 = lats1[yellow2]

# make new longs list with index list corresponding to yellow dose data values
for lonnn in longs1:
    longs12 = longs1[yellow2]

# make new yellow dose list to be used for pandas dataframe    
for ydose in dose2:
    yellow_dose2 = dose2[yellow2] 
 
# pandas data fram with yellow data    
yellow_area2 = pd.DataFrame({
    'lats2': lats12,
    'lons2': longs12,
    'dose': yellow_dose2
})

# check for values less than 1 rem and greater than 0.1 rem (100 millirem) in dose data
green2 = np.where((dose2 < 1) & (dose2 > 0.1))

# make new lats list with index list corresponding to green dose data values
for lassss in lats1:
    lats13 = lats1[green2]

# make new longs list with index list corresponding to green dose data values
for lonnnn in longs1:
    longs13 = longs1[green2]
    
# make new green dose list to be used for pandas dataframe    
for gdose in dose2:
    green_dose2 = dose2[green2] 

# pandas data fram with green data    
green_area2 = pd.DataFrame({
    'lats3': lats13,
    'lons3': longs13,
    'dose': green_dose2
})

#################### Adding the Child Thyroid colored circles to the map ##############

# add marker one by one on the map
for i in range(0,len(red_area2)):
    FG_Child.add_child(folium.Circle(
      location=[red_area2.iloc[i]['lats'], red_area2.iloc[i]['lons']],
      popup=red_area2.iloc[i]['dose'],
      radius=50,
      color="red",
      fill=True,
      fill_color="red"
   ))
    
# add marker one by one on the map
for i in range(0,len(orange_area2)):
    FG_Child.add_child(folium.Circle(
      location=[orange_area2.iloc[i]['lats1'], orange_area2.iloc[i]['lons1']],
      popup=orange_area2.iloc[i]['dose'],
      radius=50,
      color="orange",
      fill=True,
      fill_color="orange"
   ))

# add marker one by one on the map
for i in range(0,len(yellow_area2)):
    FG_Child.add_child(folium.Circle(
      location=[yellow_area2.iloc[i]['lats2'], yellow_area2.iloc[i]['lons2']],
      popup=yellow_area2.iloc[i]['dose'],
      radius=50,
      color="yellow",
      fill=True,
      fill_color="yellow"
   ))
    
# add marker one by one on the map
for i in range(0,len(green_area2)):
    FG_Child.add_child(folium.Circle(
      location=[green_area2.iloc[i]['lats3'], green_area2.iloc[i]['lons3']],
      popup=green_area2.iloc[i]['dose'],
      radius=50,
      color="green",
      fill=True,
      fill_color="green"
   ))
    
############### Emergency Worker Dose Area #############
    
# dose data update
dose3 = (np.asarray(ted_total)).flatten()

# check for values greater than 25 rem in dose data
red3 = np.where(dose3 > 25)

# make new lats list with index list corresponding to 5 rem dose data values
for las in lats1:
    lats14 = lats1[red3]
    
# make new longs list with index list corresponding to 5 rem dose data values
for lon in longs1:
    longs14 = longs1[red3]    

# make new red dose list to be used for pandas dataframe       
for rdose in dose3:
    red_dose3 = dose3[red3]

# make new red dose list to be used for pandas dataframe        
red_area3 = pd.DataFrame({
    'lats': lats14,
    'lons': longs14,
    'dose': red_dose3
})
  
# check for values less than or equal to 25 rem and greater than 10 rem in dose data
orange3 = np.where((dose3 <= 25) & (dose3 > 10))

# make new lats list with index list corresponding to orange dose data values
for lass in lats1:
    lats15 = lats1[orange3]

# make new longs list with index list corresponding to orange dose data values
for lonn in longs1:
    longs15 = longs1[orange3]   
    
# make new orange dose list to be used for pandas dataframe        
for odose in dose3:
    orange_dose3 = dose3[orange3]

# pandas data fram with orange data    
orange_area3 = pd.DataFrame({
    'lats1': lats15,
    'lons1': longs15,
    'dose': orange_dose3
})  
    
# check for values less than or equal to 10 rem and greater than 5 rem in dose data
yellow3 = np.where((dose3 <= 10) & (dose3 > 5))
    
# make new lats list with index list corresponding to yellow dose data values
for lasss in lats1:
    lats16 = lats1[yellow3]

# make new longs list with index list corresponding to yellow dose data values
for lonnn in longs1:
    longs16 = longs1[yellow3]

# make new yellow dose list to be used for pandas dataframe    
for ydose in dose3:
    yellow_dose3 = dose3[yellow3] 
 
# pandas data fram with yellow data    
yellow_area3 = pd.DataFrame({
    'lats2': lats16,
    'lons2': longs16,
    'dose': yellow_dose3
})

# check for values less than or equal to 5 rem and greater than 0.1 rem (100 millirem) in dose data
green3 = np.where((dose3 <= 5) & (dose3 > 0.1))

# make new lats list with index list corresponding to green dose data values
for lassss in lats1:
    lats17 = lats1[green3]

# make new longs list with index list corresponding to green dose data values
for lonnnn in longs1:
    longs17 = longs1[green3]
    
# make new green dose list to be used for pandas dataframe    
for gdose in dose3:
    green_dose3 = dose3[green3] 

# pandas data fram with green data    
green_area3 = pd.DataFrame({
    'lats3': lats17,
    'lons3': longs17,
    'dose': green_dose3
})

#################### Adding the Emergency Worker colored circles to the map ##############

# add marker one by one on the map
for i in range(0,len(red_area3)):
    FG_EM.add_child(folium.Circle(
      location=[red_area3.iloc[i]['lats'], red_area3.iloc[i]['lons']],
      popup=red_area3.iloc[i]['dose'],
      radius=50,
      color="red",
      fill=True,
      fill_color="red"
   ))
    
# add marker one by one on the map
for i in range(0,len(orange_area3)):
    FG_EM.add_child(folium.Circle(
      location=[orange_area3.iloc[i]['lats1'], orange_area3.iloc[i]['lons1']],
      popup=orange_area3.iloc[i]['dose'],
      radius=50,
      color="orange",
      fill=True,
      fill_color="orange"
   ))

# add marker one by one on the map
for i in range(0,len(yellow_area3)):
    FG_EM.add_child(folium.Circle(
      location=[yellow_area3.iloc[i]['lats2'], yellow_area3.iloc[i]['lons2']],
      popup=yellow_area3.iloc[i]['dose'],
      radius=50,
      color="yellow",
      fill=True,
      fill_color="yellow"
   ))
    
# add marker one by one on the map
for i in range(0,len(green_area3)):
    FG_EM.add_child(folium.Circle(
      location=[green_area3.iloc[i]['lats3'], green_area3.iloc[i]['lons3']],
      popup=green_area3.iloc[i]['dose'],
      radius=50,
      color="green",
      fill=True,
      fill_color="green"
   ))

Rad_Map.save("index.html")

# %%
