from random import random
from numpy import array
from bokeh.layouts import column
from bokeh.models import Button
from bokeh.palettes import RdYlBu3
from bokeh.plotting import figure, curdoc
import dateutil.parser

from fda import *
from plotters import *

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

#queries
far = frequentAdverseReactions()

#bar, source = vBar(far['x'], far['y'])
#bar, source = hbar(array(far['y']), array(range(1, len(far['x']))), array(far['y']))
#plot = figurePlot(array(far['y']), array(range(1, len(far['x']))), array(far['y']))
#plot = figurePlot(far['x'], far['y'])
dates = dateOfCreatedReport()
print(dates['x'])
print(dateutil.parser.parse(dates['x'][1]))
formattedDates = list(map(lambda x: dateutil.parser.parse(x), dates['x']))
print(formattedDates)
plot = figureSingleLine(formattedDates, dates['y'])

# put the button and plot in a layout and add to the document
#curdoc().add_root(column(button, p))

ex, dataSoruce = example(far)

# create a callback that will add a number in a random location
def callback():
    data = frequentAdverseReactions(fromDate='20160101', toDate='20170101')
    # BEST PRACTICE --- update .data in one step with a new dict
    dataSoruce = dict()
    new_data['x'] = ds.data['x'] + [random()*70 + 15]
    new_data['y'] = ds.data['y'] + [random()*70 + 15]
    new_data['text_color'] = ds.data['text_color'] + [RdYlBu3[i%3]]
    new_data['text'] = ds.data['text'] + [str(i)]
    ds.data = new_data

# add a button widget and configure with the call back
button = Button(label="Press Me")
button.on_click(callback)


# put the button and plot in a layout and add to the document
#curdoc().add_root(column(button, p))

ex = example(far)
curdoc().add_root(column(button, plot))

args = curdoc().session_context.request.arguments

try:
  N = int(args.get('N')[0])
except:
  N = 200