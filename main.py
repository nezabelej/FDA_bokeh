from bokeh.layouts import column
from bokeh.models import *
from bokeh.plotting import curdoc
import dateutil.parser

from fda import *
from plotters import *

#queries
far = frequentAdverseReactions()
dates = dateOfCreatedReport()
products = typesOfReportedProducts()

formattedDates = list(map(lambda x: dateutil.parser.parse(x), dates['x']))
plot, ds1 = figureSingleLine(formattedDates, dates['y'])

ex, ds2 = plotHBar(far)

plot3, dataProducts = plotHBar(products)

# create a callback that will add a number in a random location
def callback():
    data = frequentAdverseReactions(fromDate='20160101', toDate='20170101')
    ds2.data['right'] = data['y']

def productsChange():
    data = typesOfReportedProducts(productTypesSelections[selector.value])
    dataProducts.data['right'] = data['y']


# add a button widget and configure with the call back
button = Button(label="Press Me")
button.on_click(callback)


datePicker = DatePicker(width=100,title="Start date", max_date=dateutil.parser.parse('20170101'), min_date=dateutil.parser.parse('20160101'), value=dateutil.parser.parse('20160101'))
dateSlider = Slider(width=200, start=2004, end=2017, step=1)

productTypesSelections = {'All adverse event reports': '',
                          'Resulting in a serious injury or illness': 'serious',
                          'Resulting in hair loss': 'hairLoss'}

selector = Select(height=50, width=100, value='All adverse event reports',
                  options=['All adverse event reports',
                           'Resulting in a serious injury or illness',
                           'Resulting in hair loss'])
selector.on_change('value', lambda attr, old, new: productsChange())
hbox = VBox(selector, plot3)

curdoc().add_root(column(hbox))
curdoc().add_root(column(plot))
curdoc().add_root(column(button, ex))

args = curdoc().session_context.request.arguments
