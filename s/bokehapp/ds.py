#%%
import numpy as np 
import panel as pn
from ui import GUI
pn.extension()


class Dose(GUI):
    '''this will output dose.tedi, dose.tedn. dose.tedp, adult and child'''
    def __init__(self):
        FIT_DICT = {'A':1,  'B':2,  'C':3,  'D':4,  'E':5,  'F':6,  'G':7}
        self.fit = int(FIT_DICT[self.p_fit])
 
    ########################################################
    # Iodines fit function                                 #
    # these fit equations were created using MATLAB cftool #
    # self.p_hup = self.p_hup time                                 #
    # self.p_tdel = self.p_tdel time                             #
    # self.p_iodine = Iodines release rate                   #
    # tedi= TED dose                                       #
    # adult = adult dose                                   #
    # child = child dose                                   #
    ########################################################

    def iodines(self):
        self.tedi = (-7036 * np.exp(-.4306 * self.p_hup) + (-3.426e4) * np.exp(-.009497 * self.p_hup) + 5.838e4 * np.exp(
            3.875e-4 * self.p_hup)) * self.p_iodine * (100 ** 3) * self.p_tdel
        self.adult = (1.133e6 * np.exp((3.455e-4) * self.p_hup) - 1.504e5 * np.exp(-.2328 * self.p_hup) - 6.953e5 * np.exp(
            -.008704 * self.p_hup)) * self.p_iodine * (100 ** 3) * self.p_tdel
        self.child = (2.047e6 * np.exp(4.467e-4 * self.p_hup) - 2.576e5 * np.exp(-.4386 * self.p_hup) - 1.191e6 * np.exp(
            -.01076 * self.p_hup)) * self.p_iodine * (100 ** 3) * self.p_tdel
        
    ########################################################
    # Cesiums function                                     #
    # self.p_tdel = self.p_tdel time                             #
    # self.p_partic = Cesiums release rate                   #
    # tedp= TED dose                                       #
    ########################################################

    def particulates(self):
        self.tedp = 4.3e4 * self.p_partic * (100 ** 3) * self.p_tdel
        
    ########################################################
    # Nobles fit function                                  #
    # these fit equations were created using MATLAB cftool #
    # self.p_noble = Noble release rate                      #
    # self.p_hup = self.p_hup time                                 #
    # self.p_tdel = self.p_tdel time                             #
    # tedn= TED dose                                       #
    ########################################################

    def nobles(self):
        if self.p_hup == 0:
            l_holdup = 0
        else:
            l_holdup = np.log(self.p_hup)

        if self.p_tdel == 0:
            l_exposure = 0
        else:
            l_exposure = np.log(self.p_tdel)

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

        self.tedn = (p00 + p10 * l_exposure + p01 * l_holdup + p20 * l_exposure ** 2 + p11 * l_exposure * l_holdup + p02 * l_holdup ** 2 + p30 * l_exposure ** 3 + p21 * l_exposure ** 2 * l_holdup + p12 * l_exposure * l_holdup ** 2 + p03 * l_holdup ** 3 + p31 * l_exposure ** 3 * l_holdup
                + p22 * l_exposure ** 2 * l_holdup ** 2 + p13 * l_exposure * l_holdup ** 3 + p04 * l_holdup ** 4) * self.p_noble * (100 ** 3) * self.p_tdel

        
 
    

# %%
