from fda import *
from plotters import *

def frequentReactions():
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
