''' Handles different UI needs'''
from bokeh.io import curdoc
from bokeh.layouts import Column
import ipywidgets as ipw
import requests as rq 
import pandas as pd
import numpy as np
import panel as pn
import param

css = '''
.bk.panel-widget-box {
background: #fcf2c93d;
border-radius: 5px;
border: 1px black solid;
color: #251010;
}
.bk.panel-widget-box:hover {
background: whitesmoke
}
'''

pn.extension('ipywidgets', raw_css=[css])

class PMR(param.Parameterized):
    '''Set parameters to make panels'''
    df = pd.read_csv('https://rpdash.sfo3.cdn.digitaloceanspaces.com/static/in.csv', index_col=0)
    dexdict = df.T.to_dict()
    reactors = list(df.index)
       
    '''reactor'''
    p_rctr  = param.List(reactors, item_type=str)
    p_ht = param.Integer(10, label="Release Height (m):", bounds=(0,25), doc="stack height or number hours", precedence=0.11)
    p_x = param.Number(default=float(dexdict['Palo Verde']['lat']), label='Lat')
    p_y = param.Number(default=float(dexdict['Palo Verde']['lon']), label='Long')
    """atmosphere"""
    p_mu = param.Number(0, label="u ", bounds=(0.00, 25.00), doc="speed of wind at 10m", precedence=0.10)
    p_lid = param.Integer(300, label="Atmospheric Mixing Lid Height (m): ", bounds=(300,5000), step=100, doc="mixing lid height step of 100m", precedence=0.15)
    #p_fit = param.Selector(objects=fit_dict, default=1, label="Atmospheric Stability Class (A-G): ", doc="atmospheric stability class", precedence=0.05)
    """release factors"""
    p_hup = param.Number(0.5, label="Reactor Holdup Time (hrs):", bounds=(0, 4), step=0.25, doc="hold-up time 15 minute steps", precedence=0.19)
    p_src = param.Selector(objects=['Noble Gas','Iodine','Particulate'], default='Noble Gas', label="Source Release Rates (Ci/s) for ", precedence=0.3)
    p_tdel = param.Number(3, label="Release Duration (hrs): ", bounds=(0,24), doc="total exposure time", precedence=0.21)
    """User settings type pmr"""
    p_bool = param.Boolean(False, bounds=(0, 1), precedence=0.06)
    p_lidu = param.Selector(objects=['x100ft','x100m'], default='x100m', label="Mixing Lid")
    p_windu = param.Selector(objects=['w13u=0','w13u=1','w13u=2','w13u=3'], default='w13u=1', label="Surface Wind")
    #p_color = param.List(colors, item_type=str)
    p_tick = param.Number(5)
    p_sigma = param.Tuple(default=(0.0, 0.0), length=2) #some constants

class GUI(PMR):
    areas = pn.widgets.CheckButtonGroup.from_param(PMR.param.p_color, value=['red', 'orange', 'yellow'])
    tick_marks = pn.widgets.IntInput.from_param(PMR.param.p_tick)
    reactor = pn.widgets.AutocompleteInput.from_param(PMR.param.p_rctr, case_sensitive=False, value='Palo Verde', name='Nuclear Reactor', placeholder='ex: Palo Verde')
    stb_class = pn.widgets.RadioBoxGroup.from_param(PMR.param.p_fit, inline = True, width_policy='min')
    unit_toggle = ipw.ToggleButton(description='Metric', disabled=False, button_style='', align='center', tooltip='Metric', icon='check', width_policy = 'min')
    h_lid = pn.widgets.IntInput.from_param(PMR.param.p_lid, placeholder='x100m')
    xs = pn.indicators.Number.from_param(PMR.param.p_x, font_size='12pt', align='center')
    ys = pn.indicators.Number.from_param(PMR.param.p_y, font_size='12pt', align='center')
    holdup = pn.widgets.FloatInput.from_param(PMR.param.p_hup)
    exposure = pn.widgets.IntInput.from_param(PMR.param.p_tdel)
    iodine_rate = pn.widgets.FloatInput(name='Iodine', value=10, start=0, end=100)
    noble_rate= pn.widgets.FloatInput(name='Noble Gas', value=200, start=0,end=1000)
    partic_rate= pn.widgets.FloatInput(name='Particulates', value=1, start=0,end=10)
    h_release = pn.widgets.FloatInput.from_param(PMR.param.p_ht)
    wind_speed = pn.widgets.FloatInput.from_param(PMR.param.p_mu, name='Velocity (m/s):')
    #reactor.link(PMR.p_rctr, value='object')    
    timeday = pn.widgets.Select(value=12, name='Hour (24):', options=list(range(24)))
    bearing = pn.widgets.FloatInput(name='Bearing:', step=22.5, start=0, end=337.5)
    clouds = pn.widgets.Number(name='Cloudiness') 
    
    @pn.depends('xs', 'ys', watch=True)
    def get_wind(self):
        a = {'E':0,'ESE': 22.5,'SE':45, 'SSE': 67.5, 'S':90, 'SSW': 112.5, 'SW':135, 'WSW': 157.5, 
        'W':180, 'WNW':202.5, 'NW':225, 'NNW':247, 'N': 270, 'NNE': 292.5, 'NE':315, 'ENE': 337.5}
        r = np.radians(list(a.values()))
        r_cos = np.cos(r) 
        r_sin = np.sin(r) 
        json = {
            'w3':'sfcwind', 
            'w4':'sky', 
            'w6':'rh', 
            'w14':'ft20w',
            'AheadHour':'0', 
            'Submit':'Submit', 
            'FcstType':'digital',
            'textField1': self.xs.value,
            'textField2': self.ys.value,
            'site':'psr'
            }

        URL = 'http://forecast.weather.gov/MapClick.php?'
        response = rq.get(URL, json)

        df = (pd.read_html(response.text, index_col=0)[7].dropna(axis=0,how='any',thresh=None)[:4].T)
        windy = df.set_index(df.columns[0]).T.to_dict()
        u, b, c = list(windy[str(self.timeday.value)].items()) 
        b = a[b[1]]

        return u, b, c, r_cos, r_sin