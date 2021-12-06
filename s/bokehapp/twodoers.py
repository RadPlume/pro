# %%
'''Brought to you by TwoDoers, "Lead through doing'''
from dataclasses import dataclass
import numpy as np
from param import Range
from ui import GUI
from config import FIT_ARRAY, GRID, X, Y, R
from typing import Tuple, List, Any

class CalcFast:
    def __init__(self, fit: Any = GUI.fit, fitter: Any = FIT_ARRAY):
        self.fit = fit
        self.fitter = fitter
        self.Xval, self.Yval = np.meshgrid(X, Y)

@dataclass        
class Sigma:
    '''Define and get values for sigma variables''' 
    ticks: int = GUI.tick_marks.value
    grid: float = GRID        
    sigma_xyz: Tuple[str] = ('sigma_%s, ' % ('x','y','z'))

    
    @property
    def sigma_xyz(cls):
        cls.get_sigma_xyz()
        pass
    

    def get_sigma_xyz(self):
        sigma = self.fitter(np.arange(-self.GRID, self.GRID + 1, self.ticks))
        [self.sigma_y, self.sigma_z] = sigma
        return sigma
    
    @classmethod    
    def _define_limit(cls):
        r =  1 / (cls.lid * np.sqrt(2*np.pi))
        k = 1 / (np.pi * cls.fitter[1]) 
        k2 = k * np.exp(-0.5*(cls.lid/cls.fitter[1])**2)
        
        cls.limited_grid = np.where(r <= k, k2, r)
        

    
class Dose(Sigma):
    doseEq_total: List
    thyroid_total: Tuple[List, List] 
    lid: int = GUI.h_lid.value        
    
    def __init__(self):    
        self.num = (np.exp(-0.5*self.Yval/sigma_y)**2 * np.exp(-0.5*self.lid/sigma_z)**2 ) 
        self.den = np.pi*sigma_y*(sigma_z)
# %%
ted = Dose


class Models:
    puff_length = round(wind_speed, intervals * (num_moved)
    for startdex != 0 
                        distance <= GL  
                        distance + puff_length <-gl