""" Handles different UI needs"""
# %%
from datetime import datetime
import ipywidgets as ipw, requests as rq, pandas as pd, numpy as np, panel as pn, param
from config import COLORS, URL, BEARING, FIT_DICT, wind_toggle, lid_toggle
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
    bearing_dict = BEARING
    FIT_DICT = {'A':1,  'B':2,  'C':3,  'D':4,  'E':5,  'F':6,  'G':7}
    df = pd.read_csv('https://rpdash.sfo3.cdn.digitaloceanspaces.com/static/in.csv', index_col=0)
    dexdict = df.T.to_dict()
    reactors = list(df.index)    
    p_rctr = param.List(reactors, item_type=str)  
    p_x = param.Number(default=list(dexdict['Palo Verde'].values())[0], label='Lat')
    p_y = param.Number(default=list(dexdict['Palo Verde'].values())[1], label='Long')
    p_tick = param.Number(5)
    '''for reactor release parameters'''
    p_hup = param.Number(0.5, label='Reactor Holdup Time (hrs):', bounds=(0, 4), step=0.25, doc='hold-up time 15 minute steps', precedence=0.19)
    p_iodine = param.Number(10, label='Iodine rate', bounds=(0,50), step=0.5)
    p_noble = param.Number(200, label='Iodine rate', bounds=(0,1000), step=1)
    p_partic = param.Number(1, label='Iodine rate', bounds=(0,10), step=0.05)
    p_ht = param.Integer(10, label='Release Height (m):', bounds=(0, 500), doc='stack height or number hours', precedence=0.11)
    p_mu = param.Number(0, label='u ', bounds=(0.00, 25.00), doc='speed of wind at 10m', precedence=0.1)
    p_fit = param.Selector(objects=FIT_DICT.keys(), default='C', label='Atmospheric Stability Class (A-G): ', doc='atmospheric stability class', precedence=0.05)
    p_lid = param.Integer(800, label='Atmospheric Mixing Lid Height (m): ', bounds=(300, 5000), step=100, doc='mixing lid height step of 100m', precedence=0.15)       
    '''selections'''
    p_lidu = param.Selector(objects=list(lid_toggle.values()), default='x100m', label='Mixing Lid')
    p_windu = param.Selector(objects=list(wind_toggle.keys()), default='m/s', label='Surface Wind')
    p_color = param.Selector(objects=list(COLORS.keys()))
    p_src = param.Selector(objects=['Noble Gas', 'Iodine', 'Particulate'], default='Noble Gas', label='Source Release Rates (Ci/s) for ', precedence=0.3)
    p_bool = param.Boolean(False, bounds=(0, 1), precedence=0.06)
    '''time'''
    p_hour = param.Time(until=24, timestep=1, label='Current hour')
    p_minute = param.Time(until=60, timestep=5, label='Current minute')
    p_tdel = param.Number(3, label='Release Duration (hrs): ', bounds=(0, 24), doc='total exposure time', precedence=0.21)

class GUI(PMR):
    tick_marks = pn.widgets.IntInput.from_param(PMR.param.p_tick)
    areas = pn.widgets.CheckButtonGroup.from_param((PMR.param.p_color), value=['red', 'orange', 'yellow'])
    reactor = pn.widgets.AutocompleteInput.from_param((PMR.param.p_rctr), case_sensitive=False, value='Palo Verde', name='Nuclear Reactor', placeholder='ex: Palo Verde')    
    stb_class = pn.widgets.RadioBoxGroup.from_param((PMR.param.p_fit), inline=True, width_policy='min')
    unit_toggle = ipw.ToggleButton(description='Metric', disabled=False, button_style='', align='center', tooltip='Metric', icon='check', width_policy='min')     
    h_lid = pn.widgets.IntInput.from_param((PMR.param.p_lid), placeholder='x100m')
    xs = pn.indicators.Number.from_param((PMR.param.p_x), font_size='12pt', align='center')
    ys = pn.indicators.Number.from_param((PMR.param.p_y), font_size='12pt', align='center')
    holdup = pn.widgets.FloatInput.from_param(PMR.param.p_hup)
    exposure = pn.widgets.IntInput.from_param(PMR.param.p_tdel)
    iodine_rate = pn.widgets.FloatInput.from_param(PMR.param.p_iodine, name='Iodine', value=10, start=0, end=100)
    noble_rate = pn.widgets.FloatInput.from_param(PMR.param.p_noble, name='Noble Gas', value=200, start=0, end=1000)
    partic_rate = pn.widgets.FloatInput.from_param(PMR.param.p_partic, name='Particulates', value=1, start=0, end=10)
    h_release = pn.widgets.FloatInput.from_param(PMR.param.p_ht)
    wind_speed = pn.widgets.FloatInput.from_param((PMR.param.p_mu), name='Velocity (m/s):')
    timeday = pn.widgets.Select(value=(datetime.now().hour), name='Hour (24):', options=(list(range(24))))
    bearing = pn.widgets.FloatInput(value=PMR.bearing_dict['E'], name='Bearing:', step=22.5, start=0, end=337.5)
    clouds = pn.widgets.Number(name='Cloudiness')
    fit = PMR.FIT_DICT[PMR.p_fit]
    @pn.depends('xs', 'ys', watch=True)
    def get_wind(self):
        json = {'w3':'sfcwind',  'w4':'sky',  'w6':'rh',  'w14':'ft20w',  'AheadHour':'0',  'Submit':'Submit',  'FcstType':'digital',
         'site':'psr',  'textField1':self.xs.value, 'textField2':self.ys.value}
        
        response = rq.get(URL, json)
        df = pd.read_html((response.text), index_col=0)[7].dropna(axis=0, how='any', thresh=None)[:4].T
        windy = df.set_index(df.columns[0]).T.to_dict()
        if self.timeday.value < 10:
            fixme = list(windy.values())[0]
            u, b, c = list(fixme.values())
            b = self.bearing_dict[b]
            return (u, b, c)
        u, b, c = windy[str(self.timeday.value)].values()
        b = self.bearing_dict[b]
        return (u, b, c)

    def __init__(self, **params):
        super(GUI, self).__init__(**params)
        latitude, longitude = self._update_xy()
        self.xs.value = latitude
        self.ys.value = longitude
        u, b, c = self.get_wind()
        self.wind_speed.value = float(u)
        self.bearing.value = b
        self.radians = np.radians(b)
        self.degrees = b
        self.clouds.value = float(c)
        self.row = pn.Row(self.xs, self.ys, self.bearing)
        self.uipanel = pn.WidgetBox(self.reactor, self.row, self.stb_class, self.wind_speed, 
                                    self.bearing, self.h_release, self.h_lid, self.holdup, 
                                    self.exposure, height_policy='max', width_policy='min') 
        css_classes=['panel-widget-box']

    @pn.depends('reactor', watch=True)
    def _update_xy(self):
        latitude = list(PMR.dexdict['Palo Verde'].values())[0]
        longitude = list(PMR.dexdict['Palo Verde'].values())[1]
        return (latitude, longitude)


ui = GUI()

# %%
