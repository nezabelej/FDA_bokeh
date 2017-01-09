from bokeh.plotting import figure
from bokeh.models import *


def figureSingleLine(x,y, title):

    hover = HoverTool(tooltips = [("(x,y)", "($x, $y)")])
    p = figure(title=title, plot_width=400, plot_height=400, tools=[hover], x_axis_type='datetime')
    line = p.line(x, y, line_width=2, color="#7FC97F")
#    yaxis.formatter.use_scientific = False
    #povej da je y date mogoce
    return p, line.data_source


def plotHBar(data, title):

    keys = data['x']
    p = figure(title=title, width=500, height=350, y_range=keys)
    yaxis = p.select(dict(type=Axis, layout="below"))[0]
    yaxis.formatter.use_scientific = False
    hbar = p.hbar(y=range(1, len(data['x']) + 1), height=0.04, right=data['y'])

    return p, hbar.data_source