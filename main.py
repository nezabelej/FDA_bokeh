from bokeh.models import *
from bokeh.plotting import curdoc
import dateutil.parser
from bokeh.layouts import layout, widgetbox
from fda import *
from plotters import *
from counts import countsBefore
import numpy as np


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

#1.povecaj na 12 zdravil, shrani rezultat!
#2.sami s sabo imajo najvecjo stevilo? preveri
#3.sami s sabo -> grey!
#2.hoverTool
#3.polepsaj kodo

#dobi 10 najpogostejsih zdravil
drugs = frequentDrugs()
counts = np.zeros((10,10))

i=0
j=0
xname = []
yname = []
color = []
colormap = ["#abefa0", "#54af46", "#215b18"]
alpha = []

# for d1 in drugs:
#     j = 0
#     for d2 in drugs:
#         if d1 == d2:
#             counts[i,j] = 0
#         else:
#             counts[i, j] = countReactionsInCombination(d1, d2)
#         j = j + 1
#     i = i + 1

#Instead of 100 queries we use data queried from before
counts = countsBefore

min = np.amin(counts)
max = np.amax(counts)

i=0
for d1 in drugs:
    j = 0
    for d2 in drugs:
        xname.append(d1)
        yname.append(d2)
        alpha.append(np.amin([counts[i][j] / 4.0, 0.9]) + 0.1)
        if counts[i][j] == 0:
            color.append('lightgrey')
        elif counts[i][j] <= max/3:
            color.append(colormap[0])
        elif counts[i][j] <= 2*max/3:
            color.append(colormap[1])
        else:
            color.append(colormap[2])
        j = j + 1
    i = i + 1

#http://bokeh.pydata.org/en/latest/docs/gallery/les_mis.html

source = ColumnDataSource(data=dict(
    xname=xname,
    yname=yname,
    colors=color,
    alphas=alpha,
    count=counts.flatten(),
))

plotCombinations = combinationsFrequency(drugs, source)

desc = Div(text="This graph represents how many reactions were caused by the combination of two drugs", width=800)

draw([], desc, plotCombinations)
###########################################################################

curdoc().title = "FDA analysis"
args = curdoc().session_context.request.arguments
