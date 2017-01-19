import dateutil.parser
from fda import *
from plotters import *

def datesOfReports():
    dates = dateOfCreatedReport()
    formattedDates = list(map(lambda x: dateutil.parser.parse(x), dates['x']))
    plotDates, dataDates = figureSingleLine(formattedDates, dates['y'],
                                            "Adverse food, dietary supplement, and cosmetic event reports since 2004",
                                            "Year", "Number of reports")
    desc = Div(text="This is the openFDA API endpoint for adverse food, dietary supplement, "
                    "and cosmetic product events. An adverse event is submitted to the FDA to "
                    "report adverse health effects and product complaints about food, "
                    "dietary supplements, and cosmetics.", width=800)

    draw([], desc, plotDates)