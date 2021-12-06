import geoviews as gv
import geoviews.feature as gf
import xarray as xr
from cartopy import crs

import numpy as np

import datetime

import os, sys

from bokeh.io import output_file, show
from bokeh.layouts import column, widgetbox
from bokeh.plotting import figure

from bokeh.models.widgets import Button, RadioButtonGroup, Select, Slider

dataDir= "bokehapp/app/data/"

gv.extension('bokeh')
import holoviews as hv

renderer = hv.renderer('bokeh')

from bokeh.resources import CDN, INLINE
from bokeh.layouts import column, row
from bokeh.embed import components

from holoviews import opts

renderer = renderer.instance(mode='server')

import cmocean

from glob import glob

from geoviews import opts, tile_sources as gvts

from geoviews import annotate

cmapThermal = cmocean.cm.thermal

class Model(object):
    """docstring for Model"""
    def __init__(self):
        super(Model, self).__init__()
        self.butons = []

    def setValues(self, args):
        for key, value in args.items():
            exec('self.%s = %r' % (key, value))

    def setButtom(self, text):
        self.butons.append(Button(label=text))

class Ensemble(Model):
    """docstring for Ensemble"""
    def __init__(self, **kwargs):
        super(Ensemble, self).__init__()
        self.setValues(kwargs)
        self.data = xr.open_dataset(os.path.join(dataDir, self.filename))

    @property
    def dimensions(self):
        return ['longitude', 'latitude', 'time']

class LayoutDashBoard(Model):
    def __init__(self, **kwargs):
        super(LayoutDashBoard, self).__init__()
        ds = xr.open_dataset(os.path.join(dataDir, kwargs['filename']))
        long=np.linspace(-180, 180, 900, dtype='float32') 
        
        ds['longitude'] = long
        ds_out = ds.sel(latitude=slice(-22, -27), longitude=slice(-46, -41))

        dataset = gv.Dataset(ds_out, ['longitude', 'latitude', 'time'],'u10',crs=crs.PlateCarree())
        images = dataset.to(gv.Image) 
        
        im = images.opts(cmap='viridis', alpha=0.4, colorbar=True, width=600, height=500)

        self.app = im * gvts.EsriImagery