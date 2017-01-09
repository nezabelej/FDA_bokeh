from bokeh.plotting import figure
from bokeh.models import Axis


def figureSingleLine(x,y):
    p = figure(plot_width=400, plot_height=400, x_axis_type='datetime')
    line = p.line(x, y, line_width=2, color="#7FC97F")

    return p, line.data_source


def plotHBar(data):

    keys = data['x']
    p = figure(width=500, height=350, y_range=keys)
    yaxis = p.select(dict(type=Axis, layout="below"))[0]
    yaxis.formatter.use_scientific = False
    hbar = p.hbar(y=range(1, len(data['x']) + 1), height=0.04, right=data['y'])

    return p, hbar.data_source