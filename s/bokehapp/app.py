from jinja2 import Environment, FileSystemLoader
from tornado.web import RequestHandler

from bokeh.embed import server_document
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider
from bokeh.plotting import figure
from bokeh.sampledata.sea_surface_temperature import sea_surface_temperature
from bokeh.server.server import Server
from bokeh.themes import Theme

env = Environment(loader=FileSystemLoader('templates'))


from dashboard import LayoutDashBoard


import holoviews as hv
import geoviews as gv

gv.extension('bokeh')

renderer = hv.renderer('bokeh')

renderer = renderer.instance(mode='server')


class IndexHandler(RequestHandler):
    def get(self):
        template = env.get_template('embed.html')
        script = server_document('http://localhost:5006/gmap')
        self.write(template.render(script=script, template="Tornado"))

def gmap(doc):
    gvplot = LayoutDashBoard(filename="data.nc")
    renderer(gvplot.app)
    import panel as pn

    model = pn.panel(gvplot.app).get_root()
    doc.add_root(model)

server = Server({'/gmap': gmap}, allow_websocket_origin=["*"], extra_patterns=[('/', IndexHandler)])
server.start()

if __name__ == '__main__':
    from bokeh.util.browser import view
    server.io_loop.add_callback(view, "http://localhost:5006/gmap")
    server.io_loop.start()