from bokeh.models.glyphs import HBar
from bokeh.models import ColumnDataSource, DataRange1d, Plot, LinearAxis, Grid, HoverTool
from bokeh.plotting import figure, show
import pandas as pd
from bokeh.charts.attributes import CatAttr
from bokeh.charts import Bar, output_file, show
from bokeh.models import Axis


def figurePlot(x, y, yText):

    plot = figure(width=300, height=300)
    plot.hbar(right=x, y=yText, left=0, color="#7FC97F")

    show(plot)

    return plot

def barChart(x,y):


    d = {'kraji': x, 'count': y}
    print(d)

    df = pd.DataFrame(d)

    p = Bar(df, label=CatAttr(columns=['kraji'], sort=False), values='count',
            color='blue', legend=False, title='Produkcija',
            xlabel='Mesta z največjo produkcijo', ylabel='Število proizvodov')



def plotHBar(data):

    keys = data['x']
    p = figure(width=800, height=400, y_range=keys)
    yaxis = p.select(dict(type=Axis, layout="below"))[0]
    yaxis.formatter.use_scientific = False
    hbar = p.hbar(y=range(1, len(data['x']) + 1), height=0.04, right=data['y'])

    return p, hbar.data_source