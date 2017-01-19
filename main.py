from typeOfProducts import *
from frequentReactions import *
from datesOfReports import *
from combinationsDrugs import *
from citiesProduction import *
from recallByYear import *

typeOfProducts()
frequentReactions()
datesOfReports()
combinationDrugs()
citiesProduction()
recallYear()

curdoc().title = "FDA analysis"
args = curdoc().session_context.request.arguments
