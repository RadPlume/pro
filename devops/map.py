from devops.application import Application
import numpy as np
from typing import List, Dict
#-------------------------
# Globals and constants
#-------------------------

__all__ = (
    'Mapping',
    'Position',
    'Dose',
)



###############lats1, longs1, and dose need to be flattened ################
class Mapping:

    def __init__(self, latitude: array, longitude: array, dose: array):
        self.each = self.flatten()


class ExposureType:
    _total_effective_dose: List[float] = [5, 1, 0.1, 0.001]
    _adult_thyroid: List[float] = [500, 5, 1, 0.1]
    _child_thyroid: List[float] = [500, 10, 5, 0.1]
    _emergency_workers: List[float] = [25, 10, 5, 0.1]

    def __init__(self, doses: List[Dose]) -> None:
        for dose in doses:
            self._sort_doses(dose)

    def _sort_doses(self, dose: Dose) -> None:
        kwargs = dict(location = dose._location)

        def _sort(self):    
            self.color = self.dose_type
            for a, b, c, d in self.color:
                np.where(dose > )

        def sorted():
            if dose.dose_type:
               self._effective_dose_range.append(dose(_sort())) 

    
    @classmethod
    def _area(self, dose):
        color3 = np.where(dose%s % (1,2,3) > 25)      
        red_area3 = pd.DataFrame({
        'lats': lats143[color3]
        'lons': longs143[color3]
        'dose': dose143[color3]
        })


## position rotation formula
class Position:
    x_values: List[float] = []
    y_values: List[float] = []

    def __init__(self):
        X, Y = self._position_rotation()
    
    def _position_rotation(self, x_values: Array[float], y_values: Array[float], direction: float = ui.bearing)
        alpha = np.radians(direction)
        X = x_values*np.cos(alpha) + y_values/1000*np.cos(alpha)
        Y = y_values/1000*np.cos(alpha) - x_values*np.sin(alpha)
        return X, Y


    def _coordinates(self, ui, X, Y, totals: List[Dose]): -> Dose 
        radius_earth = 6371.0001
        lat = ui.xs.value + np.degrees(Y/radius_earth)
        lon = ui.ys.value + (X/radius_earth)*np.degrees(
            1 / np.cos(np.radians(ui.xs.value)))
        self.latitude = np.asarray(lat).flatten()
        self.longitude = np.asarray(lon).flatten()
        self.dose = np.asarray(total).flatten()

class Dose:
    dose_type: int

class DoseArea:
    _type_dict: Dict = {}
    _dose_type: int
    _cutoff_levels: List[str] = []
    def __init__(self):
        self._dose_type = self.Dose

    def get_cutoff_levels(self, _dose_type: str):  
        type_dict = {
            'ted': [5, 1, 0.1, 0.001], 
            'adult': [500.1, 5.001, 1.001 , 0.1],
            'child': [500.1, 10.001, 5.001 , 0.1],
            'em': [25, 10, 5, 0.1],
            }
        self._cutoff_levels = type_dict[int(_dose_type)]    
        
    # check for values greater than 5 rem in dose data\
    def color(self, color: List[str]): -> GUI
        for i in _cutoff_values[i]:
        color = np.where(dose > _cutoff_values[color])
        red_area = pd.DataFrame({
            'lats': lats1[color]
            'lons': longs1[color],
            'dose': dose[red]
        })
