from bokeh.models import *
from bokeh.plotting import curdoc
import dateutil.parser
from bokeh.layouts import layout, widgetbox
from fda import *
from plotters import *


def draw(controls, desc, plot):
    sizing_mode = 'fixed'
    inputs = widgetbox(*controls, sizing_mode=sizing_mode)
    l = layout(
        [[desc], [inputs, plot]], sizing_mode=sizing_mode)
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

desc = Div(text="Certain product types have more adverse events associated with them than others. "
                "For example, nutritional and dietary supplements have more adverse event reports, "
                "partly because manufacturers and distributors are required to report them.", width=800)

draw([selector], desc, plotProducts)
###########################################################################
far = frequentAdverseReactions()
plotReactions, dataReactions = plotHBar(far, "What adverse drug reactions are frequently reported?")

def onChangeReactions():
    data = frequentAdverseReactions(fromDate=str(dateSlider1.value)+'0101',
                                    toDate=str(dateSlider2.value)+'0101',
                                    gender=selectorGender.value)
    plotReactions.y_range.factors = data['x']
    dataReactions.data['right'] = data['y']

selectorGender = Select(title='Gender: ', value='All',
                  options=['All', 'Female', 'Male'])
selectorGender.on_change('value', lambda attr, old, new: onChangeReactions())

dateSlider1 = Slider(width=200, start=2004, end=2016, step=1, value=2004)
dateSlider2 = Slider(width=200, start=2005, end=2017, step=1, value=2017)
dateSlider1.on_change('value', lambda attr, old, new: onChangeReactions())
dateSlider2.on_change('value', lambda attr, old, new: onChangeReactions())

desc = Div(text="Adverse reactions range from product quality issues to very serious outcomes, "
                "including death. Use the buttons next to the chart to see how reported reactions "
                "vary with different search criteria.", width=800)

draw([selectorGender, dateSlider1, dateSlider2], desc, plotReactions)
###########################################################################
dates = dateOfCreatedReport()
formattedDates = list(map(lambda x: dateutil.parser.parse(x), dates['x']))
plotDates, dataDates = figureSingleLine(formattedDates, dates['y'], "Adverse food, dietary supplement, and cosmetic event reports since 2004")

desc = Div(text="This is the openFDA API endpoint for adverse food, dietary supplement, "
                "and cosmetic product events. An adverse event is submitted to the FDA to "
                "report adverse health effects and product complaints about food, "
                "dietary supplements, and cosmetics.", width=800)

draw([], desc, plotDates)
###########################################################################

###########################################################################
#dobi 10 najpogostejsih zdravil
drugs = frequentDrugs()
print (drugs)
combinations = countReactionsInCombination("BONIVA", "ROCEPHIN")
print(combinations) #stevilo pacientov z reakcijami ob tej kombinaciji

#http://bokeh.pydata.org/en/latest/docs/gallery/les_mis.html

desc = Div(text="This graph represents how many reactions were caused by the combination of two drugs", width=800)

#draw([], desc, plotCombinations)
###########################################################################

curdoc().title = "FDA analysis"
args = curdoc().session_context.request.arguments
