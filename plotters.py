from bokeh.plotting import figure
from bokeh.models import *
import numpy as np
from bokeh.layouts import layout, widgetbox
from bokeh.plotting import curdoc

def draw(controls, desc, plot):
    sizing_mode = 'fixed'
    inputs = widgetbox(*controls, sizing_mode=sizing_mode)
    l = layout(
        [[desc], [inputs, plot]], sizing_mode=sizing_mode)
    curdoc().add_root(l)

def figureSingleLine(x,y, title, xlabel, ylabel):

    hover = HoverTool(tooltips = [("(x,y)", "($x, $y)")])
    p = figure(title=title, plot_width=400, plot_height=400, tools=[hover], x_axis_type='datetime', x_axis_label=xlabel, y_axis_label=ylabel)
    line = p.line(x, y, line_width=2, color="#7FC97F")

#    yaxis.formatter.use_scientific = False
    #povej da je y date mogoce
    return p, line.data_source


def plotHBar(data, title, xlabel, ylabel):

    keys = data['x']
    p = figure(title=title, width=500, height=350, y_range=keys, x_axis_label=xlabel, y_axis_label=ylabel)
    yaxis = p.select(dict(type=Axis, layout="below"))[0]
    yaxis.formatter.use_scientific = False
    hbar = p.hbar(y=range(1, len(data['x']) + 1), height=0.04, right=data['y'])

    return p, hbar.data_source

def combinationsFrequency(names, source, xlabel, ylabel):
    p = figure(title="Frequency of reactions using the combination of drugs",
               x_axis_location="above", tools="hover,save",
               x_range=list(reversed(names)), y_range=names, x_axis_label=xlabel, y_axis_label=ylabel)

    p.plot_width = 400
    p.plot_height = 400
    p.grid.grid_line_color = None
    p.axis.axis_line_color = None
    p.axis.major_tick_line_color = None
    p.axis.major_label_text_font_size = "5pt"
    p.axis.major_label_standoff = 0
    p.xaxis.major_label_orientation = np.pi / 3

    p.rect('xname', 'yname', 0.9, 0.9, source=source,
           color='colors', alpha='alphas', line_color=None,
           hover_line_color='black', hover_color='colors')

    p.select_one(HoverTool).tooltips = [
        ('names', '@yname, @xname'),
        ('count', '@count'),
    ]

    return p


def plotBarChart(data, title):
    keys = data['x']

    p = figure(title=title, width=500, height=350, x_range=keys)
    xaxis = p.select(dict(type=Axis, layout="below"))[0]
    # xaxis.formatter.use_scientific = False
    vbar = p.vbar(x=range(1, len(data['x']) + 1), width=0.04, top=data['y'])

    return p, vbar.data_source