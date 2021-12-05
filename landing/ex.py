from param import Parameter, Parameterized, String
from panel.widgets import FloatInput, AutocompleteInput
import pandas as pd
import panel as pn

pn.extension()

class p_plant(Parameterized):
    #allows for setting map location when you click the link
    reactor = Parameter(default='Palo Verde', doc='list of reactors')
    lat = String(default="33.3881", doc='latitude of a reactor')
    long = String(default="-112.8617",  doc='longitude of a reactor') 
    placeholder = String(default=None, label="Placeholder")
    truths = Parameter(default="true", doc='string param set header true in url', constant=True)

    def __init__(self,**params):
        super(self).__init__(**params)  # Sets 

class nav_search(p_plant):
    dat = '/arcgis/home/in.csv'
    df = pd.read_csv(dat, 
    header=0, 
    dtype={
        'plantName': str,
        'latitude': str,
        'longitude': str}
    )
    reactors = list(df.plantName.values)


    aut = pn.widgets.AutocompleteInput(name='Select a Reactor (U.S.)', options=reactors).placeholders='i.e. Palo Verde'
    fl = pn.widgets.FloatInput(name='Latitude', value = 33.1, step=1e-1, start=-90, end=90)
    fl2 = pn.widgets.FloatInput(name='Longitude', value = -112.7, step=1e-1, start=-180, end=180)
    box = pn.column(aut,fl,fl2, width_policy='min')
    
    box.servable()
