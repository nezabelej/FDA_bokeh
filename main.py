from bokeh.models import *
from bokeh.plotting import curdoc
import dateutil.parser
from bokeh.layouts import layout, widgetbox
from fda import *
from plotters import *


def draw(controls, plot):
    sizing_mode = 'fixed'
    inputs = widgetbox(*controls, sizing_mode=sizing_mode)
    l = layout(
        [[inputs, plot]], sizing_mode=sizing_mode)
    curdoc().add_root(l)

##########################################################################
products = typesOfReportedProducts()
plotProducts, dataProducts = plotHBar(products, 'What types of food products are reported?')

def productsChange():
    data = typesOfReportedProducts(productTypesSelections[selector.value])
    plotProducts.y_range.factors = data['x']
    dataProducts.data['right'] = data['y']

productTypesSelections = {'All adverse event reports': '',
                          'Resulting in a serious injury or illness': 'serious',
                          'Resulting in hair loss': 'hairLoss'}

selector = Select(title='Filters:', value='All adverse event reports',
                  options=['All adverse event reports',
                           'Resulting in a serious injury or illness',
                           'Resulting in hair loss'])
selector.on_change('value', lambda attr, old, new: productsChange())

draw([selector], plotProducts)
###########################################################################

far = frequentAdverseReactions()
plotReactions, dataReactions = plotHBar(far, "What adverse drug reactions are frequently reported?")

def callback():
    data = frequentAdverseReactions(fromDate='20160101', toDate='20170101')
    plotReactions.y_range.factors = data['x']
    dataReactions.data['right'] = data['y']

def genderChange():
    data = frequentAdverseReactions(gender=selectorGender.value)
    plotReactions.y_range.factors = data['x']
    dataReactions.data['right'] = data['y']

selectorGender = Select(title='Gender: ', value='All',
                  options=['All',
                           'Female',
                           'Male'])
selectorGender.on_change('value', lambda attr, old, new: genderChange())

dateSlider1 = Slider(width=200, start=2004, end=2017, step=1)
dateSlider2 = Slider(width=200, start=2004, end=2017, step=1)

draw([selectorGender, dateSlider1, dateSlider2], plotReactions)
###########################################################################


dates = dateOfCreatedReport()
formattedDates = list(map(lambda x: dateutil.parser.parse(x), dates['x']))
plotDates, dataDates = figureSingleLine(formattedDates, dates['y'], "Adverse food, dietary supplement, and cosmetic event reports since 2004")

draw([], plotDates)
###########################################################################
curdoc().title = "FDA analysis"
args = curdoc().session_context.request.arguments
