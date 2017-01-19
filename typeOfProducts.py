from fda import *
from plotters import *

def typeOfProducts():

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