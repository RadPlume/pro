from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.models.widgets import Paragraph, Button, TextInput

button = Button(label="test me")
output = Paragraph()
into = TextInput(value="Bokeh")

def update():
    output.text = "Hello, " +  into.value

layout = column(ui, button, into, output)

curdoc().add_root()
