# %%
from datashader.tiles import render_tiles
import datashader.transfer_functions as tf
from datashader.colors import viridis
from PIL import ImageDraw
import datashader as ds 
import pandas as pd
import numpy as np
import xarray as xr
dat = 'NuclearPlants.csv'
df=pd.read_csv(dat).to_numpy()

extent_of_tile = (-50000, -50000, 50000, 50000) #xmin, ymin, xmax, ymax
cd 
df = None
def load_range(x_range, y_range):
    global df
    if df is None:
        xoffsets = [-.5, .5, -.5, .5]
        yoffsets = [-.5, .5, .5, -.5]
        xs = np.concatenate([np.random.wald(10000000, 10000000, size=10000000) * offset for offset in xoffsets])
        ys = np.concatenate([np.random.wald(10000000, 10000000, size=10000000) * offset for offset in yoffsets])
        df = pd.DataFrame(dict(x=xs, y=ys))
    
    return df.loc[df['x'].between(*x_range) & df['y'].between(*y_range)]

#%%
def rasterize(df, extent_x, extent_y, height, width):
    # aggregate
    cvs = ds.Canvas(x_range = extent_x, y_range = extent_y,
                    plot_height = height, plot_width = width)
    agg = cvs.points(df, 'x', 'y')
    return agg


def shade(agg, span=None):
    img = tf.shade(agg, cmap=reversed(viridis), span=span, how='log')
    img = tf.set_background(img, 'black')
    return img

    

def post_render(img, **kwargs):
    info = "x={},y={},z={}".format(kwargs['x'], kwargs['y'], kwargs['z'])
    draw = ImageDraw.Draw(img)
    draw.text((5, 5), info, fill='rgb(255, 255, 255)')
    return img

full_extent_of_data = (-500000, -500000, 500000, 500000)
output_path = 'tiles_output_directory/wald_tiles'
results = render_tiles(full_extent_of_data,
                       range(3),
                       load_data_func=load_range,
                       rasterize_func=rasterize,
                       shader_func=shade,
                       post_render_func=post_render,
                       output_path=output_path)


from bokeh.plotting import figure
from bokeh.models.tiles import WMTSTileSource
from bokeh.io import show
from bokeh.io import output_notebook

output_notebook()

xmin, ymin, xmax, ymax = full_extent_of_data

p = figure(width=800, height=800, 
           x_range=(int(-20e6), int(20e6)),
           y_range=(int(-20e6), int(20e6)),
           tools="pan,wheel_zoom,reset")

p.background_fill_color = 'black'
p.grid.grid_line_alpha = 0
p.axis.visible = False
p.add_tile(WMTSTileSource(url="http://localhost:8080/{Z}/{X}/{Y}.png"),
          render_parents=False)
show(p)