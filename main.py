from bokeh.layouts import column
from bokeh.models import *
from bokeh.plotting import curdoc
import dateutil.parser
from bokeh.layouts import layout, widgetbox
from fda import *
from plotters import *

#queries
far = frequentAdverseReactions()
dates = dateOfCreatedReport()
products = typesOfReportedProducts()

formattedDates = list(map(lambda x: dateutil.parser.parse(x), dates['x']))
plot, ds1 = figureSingleLine(formattedDates, dates['y'])

ex, ds2 = plotHBar(far, "What adverse reactions are frequently reported?")

plot3, dataProducts = plotHBar(products, 'What types of products are reported?')

# create a callback that will add a number in a random location
def callback():
    data = frequentAdverseReactions(fromDate='20160101', toDate='20170101')
    ex.y_range.factors = data['x']
    ds2.data['right'] = data['y']

def productsChange():
    data = typesOfReportedProducts(productTypesSelections[selector.value])
    plot3.y_range.factors = data['x']
    dataProducts.data['right'] = data['y']


# add a button widget and configure with the call back
button = Button(label="Press Me")
button.on_click(callback)


datePicker = DatePicker(width=100,title="Start date", max_date=dateutil.parser.parse('20170101'), min_date=dateutil.parser.parse('20160101'), value=dateutil.parser.parse('20160101'))
dateSlider = Slider(width=200, start=2004, end=2017, step=1)

productTypesSelections = {'All adverse event reports': '',
                          'Resulting in a serious injury or illness': 'serious',
                          'Resulting in hair loss': 'hairLoss'}

selector = Select(title='Filters:', height=50, width=100, value='All adverse event reports',
                  options=['All adverse event reports',
                           'Resulting in a serious injury or illness',
                           'Resulting in hair loss'])
selector.on_change('value', lambda attr, old, new: productsChange())
hbox = HBox(plot3, selector)

sizing_mode = 'fixed'  # 'scale_width' also looks nice with this example
controls = [selector]
inputs = widgetbox(*controls, sizing_mode=sizing_mode)
l = layout(
    [[inputs, plot3]], sizing_mode=sizing_mode)

curdoc().add_root(l)
curdoc().title = "FDA analysis"



args = curdoc().session_context.request.arguments
