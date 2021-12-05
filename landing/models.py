
import pandas as pd 
import panel as pn 
from param import Parameterized, Parameter, String, Dict
import numpy as np
pn.extension()


class p_plant(Parameterized):
    #allows for setting map location when you click the link
    reactor = Parameter(default='US/Arizona:Palo Verde', doc='list of reactors')
    lat = Parameter(default=33.3881, doc='latitude of a reactor')
    long = Parameter(default=-112.8617, doc='longitude of a reactor') 
    truths = Parameter(default="true", doc='string param set header true in url', constant=True)

    def __init__(self,**params):
        super(self).__init__(**params)  # Sets 

'''        
class nav_searchwidget(p_plant):
    indat = '/static/in.csv'
    df = pd.read_csv(indat, 
                    header=0, 
                    dtype={
                        'plantName': str,
                        'latitude': str,
                        'longitude': str}
    )

    txtsearch = pn.widgets.AutocompleteInput(
        name='Country/StateOrProvidence:Reactor', options=[df['plantName']],)
    txtin_lat = pn.widgets.FloatInput(name='Latitude', value = 33.1, step=1e-1, start=-90, end=90)
    txtin_long = pn.widgets.FloatInput(name='Longitude', value = -112.7, step=1e-1, start=-180, end=180)

    navrow = pn.Row(txtsearch, txtin_lat, txtin_long, width_policy = 'min')


class source_url(p_plant):
    src_ini = dict()

    source_url = Dict(default=src_ini)
    endpoint = String(default="https://arcgis.com/apps/Embed/index.html", doc='arcgis endpoint')
    webmap = String(default="4001d7656b0949cfa8a30a9a38b3bf91", doc='input latitude')
<<<<<<< HEAD:landing/models.py
    extent = String(default="-113.5532,33.0206,-112.7519,33.7179", doc='input longitude') 
    zoom = truths
    previewImage = truths
    scale = truths
    search =  truths
    seachextent = truths
    basemap_toggle = truths
=======
    extent = String(default="-113.5532,33.0206,-112.7519,33.7179" doc='input longitude') 
    zoom = p_plant.truths
    previewImage = p_plant.truths
    scale = p_plant.truths
    search =  p_plant.truths
    seachextent = p_plant.truths
    basemap_toggle = p_plant.truths
>>>>>>> 47be4a6de66d01dcbb64f3df7649f986a67ae483:venv/src/landing/models.py
    alt_basemap = String(default='topo')
    disable_scroll = p_plant.truths
    theme = String(default='dark')

    def __init__(self,**params):
        super(p_uri, self).__init__(**params)  # Sets 

        #self._show_navlink()

<<<<<<< HEAD:landing/models.py
    @depends("searchselect", watch=True)      # Triggers a run of the function
    def _show_navlink(self):                     # if 
        lat, long = np.where(searchselect)
=======
    #@depends("searchselect", watch=True)      # Triggers a run of the function
    
    #def _show_navlink(self):                     # if 
       # lat, long = np.where(searchselect)


class usersettings():
    location = param.
    def _get_extent(location):
>>>>>>> 47be4a6de66d01dcbb64f3df7649f986a67ae483:venv/src/landing/models.py


class mapviewer(Parameterized):
    plantsel = pn.widgets.Select(name="Reactor", options=name.cols)
    
    sli1 = pn.widgets.FloatSlider(name="time")
    sel2 = pn.widgets.Select(name="Atmospheric Stability", options=["A", "B", "C", "D", "E", "F", "G"])
    box = pn.WidgetBox("#WidgetBox", plantsel, sli1, sel2)
    index = pd.Index([p_lopts], name='rows')    
    p_sel = plantsel.value
    p_lopts = plantsel.options

    
    index.symmetric_difference(p_lopts)
    a[2]
    a[3]

    webmap = '4001d7656b0949cfa8a30a9a38b3bf91'
    extent = -113.5532,33.0206,-112.7519,33.7179
    bkin = plantsel.value

 

#class Pascy(models.Model):  
   # sigwye = models.DecimalField(max_digits=12, decimal_places=6)
    #sigzed = models.DecimalField(max_digits=12, decimal_places=6)    
#    eiks = models.IntegerField()

 #   def __str__(self):
  #      return self.sigwye, self.sigzed


   #     self._show_navlink()

<<<<<<< HEAD:landing/models.py
    @depends("searchselect", watch=True)      # Triggers a run of the function
    def _show_navlink(self):                     # if 
        lat, long = np.where(searchselect)
'''

