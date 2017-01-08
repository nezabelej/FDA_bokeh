from bokeh.plotting import figure

def figureSingleLine(x,y):
    p = figure(plot_width=400, plot_height=400, x_axis_type='datetime')

    p.line(x, y, line_width=2, color="#7FC97F")

    return p


def example(data):

    keys = data['x']
    p = figure(width=800, height=400, y_range=keys)

    hbar = p.hbar(y=range(1, len(data['x']) + 1), height=0.04, right=data['y'])

    return p, hbar.data_source