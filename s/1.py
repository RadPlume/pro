# %%
from dataclasses import dataclass 
import numpy as np
from ui import GUI
import array
from config import X, Y 

@dataclass
class Sigma(GUI):
    stability: int = GUI.fit
    downwind: float = 40.0
    
    def __init__(self):
        self.co_y = np.array([[207.473, .863316],
                         [153.669, .881424],
                         [102.77, .8974],
                         [67.2088, .902809],
                         [49.6322, .902878],
                         [33.5143, .900409]])
        self.co_z = np.array([[.225596, 2.00772, 6.04005],
                         [.0114002, 1.05809, 4.69916],
                         [-.00192604, .916609, 4.11859],
                         [-.033014, .736399, 3.4168],
                         [-.0451795, .680552, 3.05807],
                         [-.0524468, .654884, 2.61665]])
        self._get_sigma_xyz()
        
    def _get_sigma_xyz(self, stability: int = GUI.fit, downwind: float = 40.0):
        if stability < 6:
            self.sigma_y = self.sigma_x = self.co_z[stability, 0] * downwind ** (self.co_z[stability, 1])
            self.sigma_z = np.exp(self.co_z[stability, 0] * (np.log(downwind) ** 2 + self.co_z[stability, 1] *
                      np.log(downwind) + self.co_z[stability, 2]))
            self.sigma_x = self.sigma_y
        else:
            self.sigma_y = sigma_x = 2 / 3 * (self.co_y[5, 0] * downwind ** (self.co_y[5, 1]))
            self.sigma_z = 2 / 3 * (np.exp(self.co_z[5, 0] * np.log(downwind) ** 2 +
                                      self.co_z[5, 1] * np.log(downwind) + self.co_z[5, 2]))
            self.sigma_x = self.sigma_y
 

@dataclass
class DoseFunction:
    tedi: array 
    tedp: array
    tedn: array
    adult: array
    child: array

    def __init__(self):
        self.tedi = self._get_iodines().tedi
        self.adult = self._get_idiones().adult
        self.child = self._get_idiones().child

    def _get_iodines(self, ui):
        self.tedi = (-7036 * np.exp(-.4306 * ui.p_hup) + (-3.426e4) * np.exp(-.009497 * ui.p_hup) + 5.838e4 * np.exp(
            3.875e-4 * ui.p_hup)) * ui.p_iodines * (100 ** 3) * ui.p_tdel
        self.adult = (1.133e6 * np.exp((3.455e-4) * ui.p_hup) - 1.504e5 * np.exp(-.2328 * holdup) - 6.953e5 * np.exp(
            -.008704 * ui.p_hup)) * ui.p_iodines * (100 ** 3) * ui.p_tdel
        self.child = (2.047e6 * np.exp(4.467e-4 * ui.p_hup) - 2.576e5 * np.exp(-.4386 * ui.p_hup) - 1.191e6 * np.exp(
            -.01076 * ui.p_hup)) * ui.p_iodines * (100 ** 3) * ui.p_tdel
        return self.tedi, self.adult, self.child

    def nobles(self, ui):
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

        self.tedn = (p00 + p10 * l_exposure + p01 * l_holdup + p20 * l_exposure ** 2 + p11 * l_exposure * l_holdup + p02 * l_holdup ** 2 + p30 * l_exposure ** 3 + p21 * l_exposure ** 2 * l_holdup + p12 * l_exposure * l_holdup ** 2 + p03 * l_holdup ** 3 + p31 * l_exposure ** 3 * l_holdup
                + p22 * l_exposure ** 2 * l_holdup ** 2 + p13 * l_exposure * l_holdup ** 3 + p04 * l_holdup ** 4) * ui.p_nobles * (100 ** 3) * ui.p_tdel
        return self.tedn

    def particulates(self, ui):
        self.tedp = 4.3e4 * ui.p_partic * (100 ** 3) * ui.p_tdel
        return self.tedp
  
  




%% 
from dataclasses import dataclass
import numpy as np
from ui import GUI

ui = GUI()
@dataclass       
class Xcalc:
    intervals: int
    num_moves: int
    _puff_length: float
    distance: float
    
    
    @property
    def _puff_length(self, ui):
        self.wind_speed = ui.wind_speed.value
        return self.puff_length
        
    @property
    def distance(self):
        return self.distance
        
    @property
    def grid_length(self):
        return self.grid_length
        
    @_puff_length.setter
    def _puff_length(self, ui, intervals: int = 2, num_moved: int = 1):
        self.wind_speed = ui.wind_speed.value
        self.intervals = intervals
        self.num_moved = num_moved
        self._puff_length = round(ui.wind_speed.value * self.intervals * (self.num_moved + 1) * 60 / 1000, 1)
        return self.puff_length
        
    def _set_start_index(self, ui):
        self._start_index = int(round((40 + self.distance - self.puff_length/2) / (ui.tick_marks.value *.1), 1))
        return self._start_index
    
    def _set_end_index(self, ui):
        self._end_index = int(round(40 + self.distance + self.puff_length / 2, 1) / (ui.tick_marks.value * .1) + 1)
        return self._end_index
    
    def _get_index(self, ui):
        self._start_index = np.where(self.distance <= self.grid_length, self._set_start_index(), x_puff = np.zeros(1,len(x)))
        self._end_index = np.where(self.distance + self.puff_length / 2 <= self.grid_length, self._set_end_index(), _end_index = len(x_puff))
        if self._start_index != 0:
            self.x_puff[self._start_index:self._end_index] = ui.x[self._start_index:self._end_index]

# %%






