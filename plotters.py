from bokeh.models.glyphs import HBar
from bokeh.models import ColumnDataSource, DataRange1d, Plot, LinearAxis, Grid, HoverTool
from bokeh.plotting import figure, show
import pandas as pd
from bokeh.charts.attributes import CatAttr
from bokeh.charts import Bar, output_file, show
from bokeh.models import Range1d

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



def example(dataFrame, seriesName):
    this_series = dataFrame.loc[:, seriesName]
    p = figure(width=800, height=400, y_range=this_series.index.tolist())

    p.background_fill = "#EAEAF2"

    p.grid.grid_line_alpha = 1.0
    p.grid.grid_line_color = "white"

    p.xaxis.axis_label = 'Number of reactions'
    p.xaxis.axis_label_text_font_size = '4pt'
    p.xaxis.major_label_text_font_size = '4pt'


    p.yaxis.major_label_text_font_size = '2pt'
    p.yaxis.axis_label = 'Reaction'

    p.yaxis.axis_label_text_font_size = '2pt'

    maxVal = max(this_series.iteritems())[1]

    j = 1
    for k, v in this_series.iteritems():
        print(v/float(2 * maxVal))
        print(abs(v) / float(maxVal))
        p.rect(x=v/float(2 * maxVal), y=j, width=abs(v)/float(maxVal) , height=0.04, color=(76, 114, 176),
               width_units="data", height_units="data")
        j += 1

    return p