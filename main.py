from random import random
from numpy import array
from bokeh.layouts import column
from bokeh.models import Button
from bokeh.palettes import RdYlBu3
from bokeh.plotting import figure, curdoc

from fda import frequentAdverseReactions
from plotters import *
from pprint import pprint
# create a plot and style its properties
p = figure(x_range=(0, 100), y_range=(0, 100), toolbar_location=None)
p.border_fill_color = 'black'
p.background_fill_color = 'black'
p.outline_line_color = None
p.grid.grid_line_color = None

# add a text renderer to out plot (no data yet)
r = p.text(x=[], y=[], text=[], text_color=[], text_font_size="20pt",
           text_baseline="middle", text_align="center")

ds = r.data_source


from bokeh.sampledata.autompg import autompg as df

far = frequentAdverseReactions()

#bar, source = vBar(far['x'], far['y'])
#bar, source = hbar(array(far['y']), array(range(1, len(far['x']))), array(far['y']))
#plot = figurePlot(array(far['y']), array(range(1, len(far['x']))), array(far['y']))
#plot = figurePlot(far['x'], far['y'])


# put the button and plot in a layout and add to the document
#curdoc().add_root(column(button, p))

ex, dataSource = plotHBar(far)

# create a callback that will add a number in a random location
def callback():

    data = frequentAdverseReactions(fromDate='20160101', toDate='20170101')
    dataSource.data['right'] = data['y']

# add a button widget and configure with the call back
button = Button(label="Press Me")
button.on_click(callback)

curdoc().add_root(column(button, ex))


args = curdoc().session_context.request.arguments

try:
  N = int(args.get('N')[0])
except:
  N = 200