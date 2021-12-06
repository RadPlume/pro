#%% 
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
