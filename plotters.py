from bokeh.models.glyphs import HBar
from bokeh.models import ColumnDataSource, DataRange1d, Plot, LinearAxis, Grid, HoverTool
from bokeh.plotting import figure, show
import pandas as pd
from bokeh.charts.attributes import CatAttr
from bokeh.charts import Bar, output_file, show

def hbar(x,y, yText):
    N = 9
    #y = np.linspace(-2, 2, N)
    #x = y ** 3
    print (x)
    print (y)
    source = ColumnDataSource(dict(y=yText, right=x,))

    xdr = DataRange1d()
    ydr = DataRange1d()

    plot = Plot(
        title=None, x_range=xdr, y_range=ydr, plot_width=300, plot_height=300,
        h_symmetry=False, v_symmetry=False, min_border=0, toolbar_location=None)

    glyph = HBar(y="y", right="right", left=0, height=0.5, fill_color="#b3de69")
    plot.add_glyph(source, glyph)

    xaxis = LinearAxis()
    plot.add_layout(xaxis, 'below')

    yaxis = LinearAxis()
    plot.add_layout(yaxis, 'left')

    plot.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
    plot.add_layout(Grid(dimension=1, ticker=yaxis.ticker))

    return plot, source

def figurePlot(x, y, yText):

    source = ColumnDataSource(dict(y=yText, right=x ))

    xdr = DataRange1d()
    ydr = DataRange1d()
    plot = figure(width=300, height=300)
    plot.hbar(right=x, y=y, left=0, color="#7FC97F")

    show(plot)

    return plot

def barChart(x,y):


    d = {'kraji': x, 'count': y}
    print(d)

    df = pd.DataFrame(d)

    p = Bar(df, label=CatAttr(columns=['kraji'], sort=False), values='count',
            color='blue', legend=False, title='Produkcija',
            xlabel='Mesta z največjo produkcijo', ylabel='Število proizvodov')