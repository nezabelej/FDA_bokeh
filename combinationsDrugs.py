import dateutil.parser
from fda import *
from plotters import *
from counts import countsBefore
import numpy as np
from numpy import array
from datetime import *


def combinationDrugs():
    drugs = frequentDrugs()
    counts = np.zeros((10, 10))

    i = 0
    j = 0
    xname = []
    yname = []
    color = []
    colormap = ["#abefa0", "#54af46", "#215b18"]
    alpha = []

    # for d1 in drugs:
    #     j = 0
    #     for d2 in drugs:
    #         if d1 == d2:
    #             counts[i,j] = 0
    #         else:
    #             counts[i, j] = countReactionsInCombination(d1, d2)
    #         j = j + 1
    #     i = i + 1

    # Instead of 100 queries we use data queried from before
    counts = array(countsBefore)

    min = np.amin(counts)
    max = np.amax(counts)

    i = 0
    for d1 in drugs:
        j = 0
        for d2 in drugs:
            xname.append(d1)
            yname.append(d2)
            alpha.append(np.amin([counts[i, j] / 4.0, 0.9]) + 0.1)
            if counts[i, j] == 0:
                color.append('lightgrey')
            elif counts[i, j] <= max / 3:
                color.append(colormap[0])
            elif counts[i, j] <= 2 * max / 3:
                color.append(colormap[1])
            else:
                color.append(colormap[2])
            j = j + 1
        i = i + 1

    # HELP: http://bokeh.pydata.org/en/latest/docs/gallery/les_mis.html

    source = ColumnDataSource(data=dict(
        xname=xname,
        yname=yname,
        colors=color,
        alphas=alpha,
        count=counts.flatten(),
    ))

    plotCombinations = combinationsFrequency(drugs, source, "Drug name", "Drug name")

    desc = Div(text="This graph represents how many reactions were caused by the combination of two drugs", width=800)

    draw([], desc, plotCombinations)