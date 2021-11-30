######################################################################
# Radioactive Plume Visualization                              #
# By Melvin Gatewood, Michael Echeverria, Zhuo Diao, 
# Seline Ramroopsingh, & Justin Driver                                       #                           
# input variables needed
# holdup (holdup time),  exposure (exposure time), 
# iodine_rate (iodine source release rate), noble_rate(noble gas source release rate)
# partic_rate (cesiums source release rate), h_release (release height) #
# wind_speed, wind_direction, class (stability), #
# h_lid (mixing lid),plant_select (nuclear power plant selection) #
### Disclaimer - Due to programming package limitations displayed map dose values
### contain xx significant figures
######################################################################
import folium
import numpy as np 
import panel as pn
import pandas as pd
import matplotlib.pyplot as plt
from folium import plugins
from mpl_toolkits import mplot3d
import warnings

pn.extension()


######################## Begin allowable inputs #############################


##############################
# Reactor Release Parameters #
##############################

### --> Please enter reactor hold-up time (hrs)
holdup = 0.5

### --> Please enter release duration (exposure) time (hrs)
exposure = 3

### --> Please enter iodine release rate (Ci/s)
iodine_rate = 10

### --> Please enter noble gases release rate (Ci/s)
noble_rate = 200

### --> Please enter particulate (cesiums) release rate (Ci/s)
partic_rate = 1

### --> Please enter release height (m)
h_release = 10

### --> Please enter wind speed (m/s)
wind_speed = 1.788

### --> Please enter an angle value for the desired wind direction
wind_direction = 315

### if direction = E, then wind_direction = 0
### if direction = SE, then wind_direction = 45
### if direction = S, then wind_direction = 90
### if direction = SW, then wind_direction = 135
### if direction = W, then wind_direction = 180
### if direction = NW, then wind_direction = 225
### if direction = N, then wind_direction = 270
### if direction = NE, then wind_direction = 315

##############################
# Atmospheric Conditions     #
##############################

# stb_class selects which stability class to plot, A-G are 1-6 respectively
### --> Please choose an atmospheric stability class
stb_class = 3

### --> Please enter the atmospheric mixing lid height (m/s)
h_lid = 800

# Nuclear power plant data frames (No edits needed here)
df = pd.read_csv('NuclearPlants.csv')
plants = df.Plantname.to_list()
latsx = np.array(df.latitude)
longsx = np.array(df.longitude)


### --> Please make a nuclear power plant selection
# Consult with NuclearPlants file and input the corresponding index value 
# plants[index value], example --> plants[7] will select "Browns Ferry Unit 3"
plant_select = plants[52]


######################## End of allowable inputs #############################

warnings.filterwarnings("ignore")  # turn off iteration warnings
tick_marks = 5  # This variable modifies the step interval in the grid
Intervals = 2  # Interval between puffs in minutes
End_puff = 12*15  # how many puffs are to be calculated
grid_length = 40  # maximum downwind distance of grid
y = np.arange(-grid_length * 1000, grid_length * 1001, tick_marks * 100)  # in meters
x = np.arange(-grid_length, grid_length + tick_marks / 10, tick_marks / 10)  # in kilometers
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
def sigma_y_func(stb_class, x):
    if stb_class < 6:
        sigma_y = SIGMA_Y_COEF[int(stb_class), 0] * x ** (SIGMA_Y_COEF[int(stb_class), 1])
    else:
        sigma_y = 2 / 3 * (SIGMA_Y_COEF[5, 0] * x ** (SIGMA_Y_COEF[5, 1]))
    return sigma_y


#########################################################
# sigma_x function is used to calculate the sigma y fit #
# x = location in x direction                           #
# class = stability class                               #
#########################################################
def sigma_x_func(stb_class, x):
    if stb_class < 6:
        sigma_x = SIGMA_Y_COEF[int(stb_class), 0] * x ** (SIGMA_Y_COEF[int(stb_class), 1])
    else:
        sigma_x = 2 / 3 * (SIGMA_Y_COEF[5, 0] * x ** (SIGMA_Y_COEF[5, 1]))
    return sigma_x


#########################################################
# sigma_z function is used to calculate the sigma z fit #
# x = location in x direction                           #
# class = stability class                               #
#########################################################
def sigma_z_func(stb_class, x):

    if stb_class < 6:
        sigma_z = np.exp(
            SIGMA_Z_COEF[int(stb_class), 0] * (np.log(x)) ** 2 + SIGMA_Z_COEF[int(stb_class), 1] * np.log(x) +
            SIGMA_Z_COEF[int(stb_class), 2])
    else:
        sigma_z = 2 / 3 * (
            np.exp(SIGMA_Z_COEF[5, 0] * (np.log(x)) ** 2 + SIGMA_Z_COEF[5, 1] * np.log(x) + SIGMA_Z_COEF[5, 2]))
    return sigma_z


########################################################
# Iodines fit function                                 #
# these fit equations were created using MATLAB cftool #
# holdup = holdup time                                 #
# exposure = exposure time                             #
# iodine_rate = Iodines release rate                   #
# tedi= TED dose                                       #
# adult = adult dose                                   #
# child = child dose                                   #
########################################################

def iodines_func(holdup, exposure, iodine_rate, wind_speed):
    tedi = (-7036 * np.exp(-.4306 * holdup) + (-3.426e4) * np.exp(-.009497 * holdup) + 5.838e4 * np.exp(
        3.875e-4 * holdup)) * iodine_rate * (100 ** 3) * exposure
    adult = (1.133e6 * np.exp((3.455e-4) * holdup) - 1.504e5 * np.exp(-.2328 * holdup) - 6.953e5 * np.exp(
        -.008704 * holdup)) * iodine_rate * (100 ** 3) * exposure
    child = (2.047e6 * np.exp(4.467e-4 * holdup) - 2.576e5 * np.exp(-.4386 * holdup) - 1.191e6 * np.exp(
        -.01076 * holdup)) * iodine_rate * (100 ** 3) * exposure
    return tedi, adult, child


########################################################
# Nobles fit function                                  #
# these fit equations were created using MATLAB cftool #
# noble_rate = Noble release rate                      #
# holdup = holdup time                                 #
# exposure = exposure time                             #
# tedn= TED dose                                       #
########################################################

def nobles(holdup, exposure, noble_rate, wind_speed):
    if holdup == 0:
        l_holdup = 0
    else:
        l_holdup = np.log(holdup)

    if exposure == 0:
        l_exposure = 0
    else:
        l_exposure = np.log(exposure)

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


########################################################
# Cesiums function                                     #
# exposure = exposure time                             #
# partic_rate = Cesiums release rate                   #
# tedp= TED dose                                       #
########################################################

def particulates(partic_rate, exposure, wind_speed):
    tedp = 4.3e4 * partic_rate * (100 ** 3) * exposure
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

def x_calc(grid_length, num_moved, wind_speed, distance):
    x_index_start = 0
    x_index_end = 0
    x_puff = np.zeros(len(x))
    puff_length = round(wind_speed * Intervals * (num_moved + 1) * 60 / 1000, 1)

    if distance <= grid_length:  # has puff gone outside of the grid?
        x_index_start = int(round((40 + distance - puff_length / 2) / (tick_marks * .1), 1))  # calculate puff start index
    else:
        x_puff = np.zeros(1, len(x))  # it has so nothing to calculate

    if distance + puff_length / 2 > grid_length:  # is the end of the puff outside of the grid?
        x_index_end = len(x_puff)  # if so then we calculate only to the end of the grid
    else:
        x_index_end = int(round(40 + distance + puff_length / 2, 1) / (tick_marks * .1) + 1)  # calculate the end

    if x_index_start != 0:  # if the puff starts inside of the grid
        x_puff[x_index_start: x_index_end] = x[x_index_start:x_index_end]  # calculate puff parameters
    return x_puff


###################################
# TADPLUME Concentration function #
###################################

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


#######################
# Main Body of Script #
#######################

###########################################
# Generate the puffs.                     #
# right now they all have same wind speed #
# stability classes                       #
###########################################

for puff_num in np.arange(0, End_puff):
    for num_moved in np.arange(0, End_puff - puff_num):
        puff_track[puff_num, num_moved, 0] = stb_class
        puff_track[puff_num, num_moved, 1] = wind_speed
        puff_track[puff_num, num_moved, 2] = 1  # direction for future use

########################################
# Calculate concentration of each puff #
# Then add them together in order to   #
# total the concentration              #
########################################

for puff_num in np.arange(0, End_puff):
    puff_distance = 0
    num_moved = 0

    # for loop calculates distance the puff has traveled
    for num_moved in np.arange(0, End_puff - puff_num - 1):
        puff_distance = puff_distance + puff_track[
            puff_num, num_moved, 1] * Intervals * 60 / 1000  # how far will puff move

    puff_distance = round(puff_distance, 1)
    stb_class = puff_track[puff_num, num_moved, 0]  # get the current stability class for the puff
    wind_speed = puff_track[puff_num, num_moved, 1]  # get the current wind speed of the puff

    # get the puff\plume distance\length parameters
    x_puff = x_calc(grid_length, num_moved, wind_speed, puff_distance)

    # get the dispersion of the puff\plume
    if puff_num == End_puff - 1:
        concentration = plume_conc_func(x_puff, stb_class, h_lid, h_release,
                                        wind_speed)  # calculate the concentration using plume
    else:
        concentration = puff_conc_func(puff_distance, x_puff, stb_class, h_lid,
                                       h_release)  # calculate the concentration

    # Get Iodines doses #
    tedi, adult_dose, child_dose = iodines_func(holdup, exposure, iodine_rate, wind_speed)

    # Get Nobles doses #
    tedn = nobles(holdup, exposure, noble_rate, wind_speed)

    # Get Cesiums doses #
    tedp = particulates(partic_rate, exposure, wind_speed)

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
#### end dose equation part begin visualization code

# Nuclear Power plant selection

plantx = plant_select

if plantx == plants[0]:
        lat1 = latsx[0]
        long2 = longsx[0]
if plantx == plants[1]:
        lat1 = latsx[1]
        long2 = longsx[1]
if plantx == plants[2]:
        lat1 = latsx[2]
        long2 = longsx[2]
if plantx == plants[3]:
        lat1 = latsx[3]
        long2 = longsx[3]
if plantx == plants[4]:
        lat1 = latsx[4]
        long2 = longsx[4]
if plantx == plants[5]:
        lat1 = latsx[5]
        long2 = longsx[5]
if plantx == plants[6]:
        lat1 = latsx[6]
        long2 = longsx[6]
if plantx == plants[7]:
        lat1 = latsx[7]
        long2 = longsx[7]
if plantx == plants[8]:
        lat1 = latsx[8]
        long2 = longsx[8]
if plantx == plants[9]:
        lat1 = latsx[9]
        long2 = longsx[9]
if plantx == plants[10]:
        lat1 = latsx[10]
        long2 = longsx[10]
if plantx == plants[11]:
        lat1 = latsx[11]
        long2 = longsx[11]
if plantx == plants[12]:
        lat1 = latsx[12]
        long2 = longsx[12]
if plantx == plants[13]:
        lat1 = latsx[13]
        long2 = longsx[13]
if plantx == plants[14]:
        lat1 = latsx[14]
        long2 = longsx[14]
if plantx == plants[15]:
        lat1 = latsx[15]
        long2 = longsx[15]
if plantx == plants[16]:
        lat1 = latsx[16]
        long2 = longsx[16]
if plantx == plants[17]:
        lat1 = latsx[17]
        long2 = longsx[17]
if plantx == plants[18]:
        lat1 = latsx[18]
        long2 = longsx[18]
if plantx == plants[19]:
        lat1 = latsx[19]
        long2 = longsx[19]
if plantx == plants[20]:
        lat1 = latsx[20]
        long2 = longsx[20]
if plantx == plants[21]:
        lat1 = latsx[21]
        long2 = longsx[21]
if plantx == plants[22]:
        lat1 = latsx[22]
        long2 = longsx[22]
if plantx == plants[23]:
        lat1 = latsx[23]
        long2 = longsx[23]
if plantx == plants[24]:
        lat1 = latsx[24]
        long2 = longsx[24]
if plantx == plants[25]:
        lat1 = latsx[25]
        long2 = longsx[25]
if plantx == plants[26]:
        lat1 = latsx[26]
        long2 = longsx[26]
if plantx == plants[27]:
        lat1 = latsx[27]
        long2 = longsx[27]
if plantx == plants[28]:
        lat1 = latsx[28]
        long2 = longsx[28]
if plantx == plants[29]:
        lat1 = latsx[29]
        long2 = longsx[29]
if plantx == plants[30]:
        lat1 = latsx[30]
        long2 = longsx[30]
if plantx == plants[31]:
        lat1 = latsx[31]
        long2 = longsx[31]
if plantx == plants[32]:
        lat1 = latsx[32]
        long2 = longsx[32]
if plantx == plants[33]:
        lat1 = latsx[33]
        long2 = longsx[33]
if plantx == plants[34]:
        lat1 = latsx[34]
        long2 = longsx[34]
if plantx == plants[35]:
        lat1 = latsx[35]
        long2 = longsx[35]
if plantx == plants[36]:
        lat1 = latsx[36]
        long2 = longsx[36]
if plantx == plants[37]:
        lat1 = latsx[37]
        long2 = longsx[37]
if plantx == plants[38]:
        lat1 = latsx[38]
        long2 = longsx[38]
if plantx == plants[39]:
        lat1 = latsx[39]
        long2 = longsx[39]
if plantx == plants[40]:
        lat1 = latsx[40]
        long2 = longsx[40]
if plantx == plants[41]:
        lat1 = latsx[41]
        long2 = longsx[41]
if plantx == plants[42]:
        lat1 = latsx[42]
        long2 = longsx[42]
if plantx == plants[43]:
        lat1 = latsx[43]
        long2 = longsx[43]
if plantx == plants[44]:
        lat1 = latsx[44]
        long2 = longsx[44]
if plantx == plants[45]:
        lat1 = latsx[45]
        long2 = longsx[45]
if plantx == plants[46]:
        lat1 = latsx[46]
        long2 = longsx[46]
if plantx == plants[47]:
        lat1 = latsx[47]
        long2 = longsx[47]
if plantx == plants[48]:
        lat1 = latsx[48]
        long2 = longsx[48]
if plantx == plants[49]:
        lat1 = latsx[49]
        long2 = longsx[49]
if plantx == plants[50]:
        lat1 = latsx[50]
        long2 = longsx[50]
if plantx == plants[51]:
        lat1 = latsx[51]
        long2 = longsx[51]
if plantx == plants[52]:
        lat1 = latsx[52]
        long2 = longsx[52]
if plantx == plants[53]:
        lat1 = latsx[53]
        long2 = longsx[53]
if plantx == plants[54]:
        lat1 = latsx[54]
        long2 = longsx[54]
if plantx == plants[55]:
        lat1 = latsx[55]
        long2 = longsx[55]
if plantx == plants[56]:
        lat1 = latsx[56]
        long2 = longsx[56]
if plantx == plants[57]:
        lat1 = latsx[57]
        long2 = longsx[57]
if plantx == plants[58]:
        lat1 = latsx[58]
        long2 = longsx[58]
if plantx == plants[59]:
        lat1 = latsx[59]
        long2 = longsx[59]
if plantx == plants[60]:
        lat1 = latsx[60]
        long2 = longsx[60]
if plantx == plants[61]:
        lat1 = latsx[61]
        long2 = longsx[61]
if plantx == plants[62]:
        lat1 = latsx[62]
        long2 = longsx[62]
if plantx == plants[63]:
        lat1 = latsx[63]
        long2 = longsx[63]
if plantx == plants[64]:
        lat1 = latsx[64]
        long2 = longsx[64]
if plantx == plants[65]:
        lat1 = latsx[65]
        long2 = longsx[65]
if plantx == plants[66]:
        lat1 = latsx[66]
        long2 = longsx[66]
if plantx == plants[67]:
        lat1 = latsx[67]
        long2 = longsx[67]
if plantx == plants[68]:
        lat1 = latsx[68]
        long2 = longsx[68]
if plantx == plants[69]:
        lat1 = latsx[69]
        long2 = longsx[69]
if plantx == plants[70]:
        lat1 = latsx[70]
        long2 = longsx[70]
if plantx == plants[71]:
        lat1 = latsx[71]
        long2 = longsx[71]
if plantx == plants[72]:
        lat1 = latsx[72]
        long2 = longsx[72]
if plantx == plants[73]:
        lat1 = latsx[73]
        long2 = longsx[73]
if plantx == plants[74]:
        lat1 = latsx[74]
        long2 = longsx[74]
if plantx == plants[75]:
        lat1 = latsx[75]
        long2 = longsx[75]
if plantx == plants[76]:
        lat1 = latsx[76]
        long2 = longsx[76]
if plantx == plants[77]:
        lat1 = latsx[77]
        long2 = longsx[77]
if plantx == plants[78]:
        lat1 = latsx[78]
        long2 = longsx[78]
if plantx == plants[79]:
        lat1 = latsx[79]
        long2 = longsx[79]
if plantx == plants[80]:
        lat1 = latsx[80]
        long2 = longsx[80]
if plantx == plants[81]:
        lat1 = latsx[81]
        long2 = longsx[81]
if plantx == plants[82]:
        lat1 = latsx[82]
        long2 = longsx[82]
if plantx == plants[83]:
        lat1 = latsx[83]
        long2 = longsx[83]
if plantx == plants[84]:
        lat1 = latsx[84]
        long2 = longsx[84]


# After running the dose equation, the Y values need to be converted into km
newY = Yval /1000

############### Convert X and Y into lat and long coordinates #############

# radius of earth (km)
r_earth = 6371.0001


# equation to rotate plume about plant origin base on directon (angle input)
alpha = (wind_direction * (np.pi/180))

## position rotation formula
X_1 = (Xval*np.cos(alpha)) + (newY*np.sin(alpha))

Y_1 = (newY*np.cos(alpha)) - (Xval*np.sin(alpha))

#Latitude from X
for element in Y_1:
    lats = lat1 + (Y_1/r_earth)*(180/np.pi)

#Longitude from Y
for element in X_1:
    longs = long2 + (X_1/r_earth) * ((180/np.pi) / np.cos(lat1 * np.pi/180))
    
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
    location=[lat1, long2],
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

Rad_Map.save("PlumeMap.html")
