from bokeh.layouts import column
from bokeh.models import Button

from bokeh.plotting import curdoc
import dateutil.parser

from fda import *
from plotters import *

#queries
far = frequentAdverseReactions()
dates = dateOfCreatedReport()

formattedDates = list(map(lambda x: dateutil.parser.parse(x), dates['x']))
plot, ds1 = figureSingleLine(formattedDates, dates['y'])

ex, ds2 = plotHBar(far)

# create a callback that will add a number in a random location
def callback():
    data = frequentAdverseReactions(fromDate='20160101', toDate='20170101')
    ds2.data['right'] = data['y']

# add a button widget and configure with the call back
button = Button(label="Press Me")
button.on_click(callback)

curdoc().add_root(column(plot))
curdoc().add_root(column(button, ex))

args = curdoc().session_context.request.arguments
