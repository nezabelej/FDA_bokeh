from bokeh.models import *
from bokeh.plotting import curdoc
import dateutil.parser
from bokeh.layouts import layout, widgetbox
from fda import *
from plotters import *

##########################################################################
products = typesOfReportedProducts()
plotProducts, dataProducts = plotHBar(products, 'What types of products are reported?')

def productsChange():
    data = typesOfReportedProducts(productTypesSelections[selector.value])
    plotProducts.y_range.factors = data['x']
    dataProducts.data['right'] = data['y']

productTypesSelections = {'All adverse event reports': '',
                          'Resulting in a serious injury or illness': 'serious',
                          'Resulting in hair loss': 'hairLoss'}

selector = Select(title='Filters:', height=50, width=100, value='All adverse event reports',
                  options=['All adverse event reports',
                           'Resulting in a serious injury or illness',
                           'Resulting in hair loss'])
selector.on_change('value', lambda attr, old, new: productsChange())

sizing_mode = 'fixed'  # 'scale_width' also looks nice with this example
controls = [selector]
inputs = widgetbox(*controls, sizing_mode=sizing_mode)
l = layout(
    [[inputs, plotProducts]], sizing_mode=sizing_mode)
curdoc().add_root(l)
###########################################################################

far = frequentAdverseReactions()
ex, ds2 = plotHBar(far, "What adverse reactions are frequently reported?")

def callback():
    data = frequentAdverseReactions(fromDate='20160101', toDate='20170101')
    ex.y_range.factors = data['x']
    ds2.data['right'] = data['y']

button = Button(label="Press Me")
button.on_click(callback)


dateSlider = Slider(width=200, start=2004, end=2017, step=1)
###########################################################################


dates = dateOfCreatedReport()
formattedDates = list(map(lambda x: dateutil.parser.parse(x), dates['x']))
plot, ds1 = figureSingleLine(formattedDates, dates['y'])

###########################################################################
curdoc().title = "FDA analysis"
args = curdoc().session_context.request.arguments
