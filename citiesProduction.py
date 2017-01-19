from fda import *
from plotters import *

def citiesProduction():
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