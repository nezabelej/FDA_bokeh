import dateutil.parser
from fda import *
from plotters import *
from counts import countsBefore
import numpy as np
from numpy import array

##########################################################################

products = typesOfReportedProducts()
plotProducts, dataProducts = plotHBar(products, 'What types of food products are reported?', "Quantity", "Type of product")

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
plotReactions, dataAll, dataMale, dataFemale = plotHBar(far, "What adverse drug reactions are frequently reported?", "Quantity", "Reaction")

def onChangeReactions():
    data = frequentAdverseReactions(fromDate=str(dateSlider1.value)+'0101',
                                    toDate=str(dateSlider2.value)+'0101',
                                    gender=selectorGender.value)
    plotReactions.y_range.factors = data['x']
    dataAll.data['right'] = data['All']
    dataMale.data['right'] = data['Male']
    dataFemale.data['right'] = data['Female']

selectorGender = Select(title='Gender: ', value='All',
                  options=['All', 'Female', 'Male'])
selectorGender.on_change('value', lambda attr, old, new: onChangeReactions())

dateSlider1 = Slider(title='From\n', width=200, start=2004, end=2016, step=1, value=2004)
dateSlider2 = Slider(title='To\n', width=200, start=2005, end=2017, step=1, value=2017)
dateSlider1.on_change('value', lambda attr, old, new: onChangeReactions())
dateSlider2.on_change('value', lambda attr, old, new: onChangeReactions())

desc = Div(text="Adverse reactions range from product quality issues to very serious outcomes, "
                "including death. Use the buttons next to the chart to see how reported reactions "
                "vary with different search criteria.", width=800)

draw([selectorGender, dateSlider1, dateSlider2], desc, plotReactions)

###########################################################################

dates = dateOfCreatedReport()
formattedDates = list(map(lambda x: dateutil.parser.parse(x), dates['x']))
plotDates, dataDates = figureSingleLine(formattedDates, dates['y'], "Adverse food, dietary supplement, and cosmetic event reports since 2004", "Year", "Number of reports")
desc = Div(text="This is the openFDA API endpoint for adverse food, dietary supplement, "
                "and cosmetic product events. An adverse event is submitted to the FDA to "
                "report adverse health effects and product complaints about food, "
                "dietary supplements, and cosmetics.", width=800)

draw([], desc, plotDates)

###########################################################################

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
counts = array(countsBefore)

min = np.amin(counts)
max = np.amax(counts)

i=0
for d1 in drugs:
    j = 0
    for d2 in drugs:
        xname.append(d1)
        yname.append(d2)
        alpha.append(np.amin([counts[i, j] / 4.0, 0.9]) + 0.1)
        if counts[i, j] == 0:
            color.append('lightgrey')
        elif counts[i, j] <= max/3:
            color.append(colormap[0])
        elif counts[i, j] <= 2*max/3:
            color.append(colormap[1])
        else:
            color.append(colormap[2])
        j = j + 1
    i = i + 1

#HELP: http://bokeh.pydata.org/en/latest/docs/gallery/les_mis.html

source = ColumnDataSource(data=dict(
    xname=xname,
    yname=yname,
    colors=color,
    alphas=alpha,
    count=counts.flatten(),
))

plotCombinations = combinationsFrequency(drugs, source, "Drug name", "Drug name")

desc = Div(text="This graph represents how many reactions were caused by the combination of two drugs", width=800)

draw([], desc, plotCombinations)

###########################################################################
###########################################################################
# mesta z največjo produkcijo
production = productionCities()

production['x'] = [x.upper() for x in production['x']]

plotCities, dataCities = plotHBar2(production, "Which cities produce the most food products?")


def onChangeTopCities():
    data = productionCities(top=textInput.value)
    data['x'] = [x.upper() for x in data['x']]
    plotCities.y_range.factors = data['x']
    dataCities.data['right'] = data['y']

    dataCities.data['y'] = list(range(1, int(textInput.value) + 1))
    print(dataCities.data['y'])
    print(dataCities.data['right'])


textInput = TextInput(value="10", title="Number of cities:")
textInput.on_change('value', lambda attr, old, new: onChangeTopCities())

desc = Div(text="OpenFDA: Food recall enforcement reports. Food production in cities from lowest to highest.",
           width=800)

draw([textInput], desc, plotCities)
###########################################################################


###########################################################################
# odpoklic po letih
recall = recallByYear()

# print(recall)
trueX = []
trueY = []

for i in range(0, len(recall['x'])):
    year = recall['x'][i][0:4]
    # print(year)
    if (year in trueX):
        idx = trueX.index(year)
    else:
        trueX.append(year)
        idx = trueX.index(year)

    if (len(trueY) < idx + 1):
        trueY.append(1)
    else:
        trueY[idx] = trueY[idx] + 1

recall2 = {'x': trueX, 'y': trueY}

# plotRecall, dataRecall = plotBarChart(recall2, "Recall by year")
plotRecall, dataRecall = plotHBar2(recall2, "Recall by year")


def onChangeRecallDate():
    print(begin.value)
    print(end.value)
    bV = begin.value
    eV = end.value

    bVStr = bV.strftime('%Y%m%d')
    eVStr = eV.strftime('%Y%m%d')

    print(bVStr)
    print(eVStr)

    data = recallByYear(fromDate=bVStr, toDate=eVStr)

    # print(data['x'])
    # print(data['y'])

    trueX = []
    trueY = []

    for i in range(0, len(data['x'])):
        year = data['x'][i][0:4]
        # print(year)
        if (year in trueX):
            idx = trueX.index(year)
        else:
            trueX.append(year)
            idx = trueX.index(year)

        if (len(trueY) < idx + 1):
            trueY.append(1)
        else:
            trueY[idx] = trueY[idx] + 1

    data2 = {'x': trueX, 'y': trueY}

    print(data2['x'])
    print(data2['y'])

    plotRecall.y_range.factors = data2['x']
    dataRecall.data['right'] = data2['y']

    dataRecall.data['y'] = list(range(1, len(data2['x']) + 1))
    print(dataRecall.data['y'])
    print(dataRecall.data['right'])


begin = DatePicker(title="Begin Date:", min_date=datetime(2004, 1, 1),
                   max_date=datetime.now(),
                   value=datetime(datetime.now().year, 1, 1))

end = DatePicker(title="End Date:", min_date=datetime(2004, 1, 1),
                 max_date=datetime.now(),
                 value=datetime(datetime.now().year, 1, 1))

recallButton = Button(label="Show", button_type="success")
recallButton.on_click(onChangeRecallDate)

desc = Div(
    text="OpenFDA: Food recall enforcement reports. Recalls are and appropriate alternative method for removing or correcting "
         "marketed consumer products, their labeling, and/or promotional literature that violate the laws administred "
         "by the Food and Drug Administration (FDA).", width=800)

draw([begin, end, recallButton], desc, plotRecall)

###########################################################################

curdoc().title = "FDA analysis"
args = curdoc().session_context.request.arguments
