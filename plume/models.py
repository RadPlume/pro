from django.db import models
import param

class Interface(models.Model):
    
    
p_rctr  = param.List(reactors, item_type=str)
p_ht = param.Integer(10, label="Release Height (m):", bounds=(0,25), doc="stack height or number hours", precedence=0.11)
p_x = param.Number(default=float(dexdict['Palo Verde']['lat']), label='Lat')
p_y = param.Number(default=float(dexdict['Palo Verde']['lon']), label='Long')
"""atmosphere"""
p_mu = param.Number(0, label="u ", bounds=(0.00, 25.00), doc="speed of wind at 10m", precedence=0.10)
p_lid = param.Integer(300, label="Atmospheric Mixing Lid Height (m): ", bounds=(300,5000), step=100, doc="mixing lid height step of 100m", precedence=0.15)
p_fit = param.Selector(objects=fit_dict, default=1, label="Atmospheric Stability Class (A-G): ", doc="atmospheric stability class", precedence=0.05)
"""release factors"""
p_hup = param.Number(0.5, label="Reactor Holdup Time (hrs):", bounds=(0, 4), step=0.25, doc="hold-up time 15 minute steps", precedence=0.19)
p_src = param.Selector(objects=['Noble Gas','Iodine','Particulate'], default='Noble Gas', label="Source Release Rates (Ci/s) for ", precedence=0.3)
p_tdel = param.Number(3, label="Release Duration (hrs): ", bounds=(0,24), doc="total exposure time", precedence=0.21)
"""User settings type pmr"""
p_bool = param.Boolean(False, bounds=(0, 1), precedence=0.06)
p_lidu = param.Selector(objects=['x100ft','x100m'], default='x100m', label="Mixing Lid")
p_windu = param.Selector(objects=['w13u=0','w13u=1','w13u=2','w13u=3'], default='w13u=1', label="Surface Wind")
p_color = param.List(colors, item_type=str)
p_tick = param.Number(5)
p_sigma = param.Tuple(default=(0.0, 0.0), length=2) #some constants

import pandas as pd
import geopandas as gpd


df = pd.read_csv('../NuclearPlants.csv')
gdf = gpd.GeoDataFrame(df, geomerty=gpd.points_from_xy) 

# %%
import geoviews as gv


gv.extension('bokeh')

(gv.tile_sources.EsriImagery.opts(width=600, height=400,global_extent=True, title='base') * 
 gv.tile_sources.StamenLabels.options(level='annotation'))
# %%