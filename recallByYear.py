from fda import *
from plotters import *
from datetime import *

def recallYear():
    # odpoklic po letih
    recall = recallByYear()

    # print(recall)
    trueX = []
    trueY = []

    for i in range(0, len(recall['x'])):
        year = recall['x'][i][0:4]
        # print(year)
        if (year in trueX):
            idx = trueX.index(year)
        else:
            trueX.append(year)
            idx = trueX.index(year)

        if (len(trueY) < idx + 1):
            trueY.append(1)
        else:
            trueY[idx] = trueY[idx] + 1

    recall2 = {'x': trueX, 'y': trueY}

    # plotRecall, dataRecall = plotBarChart(recall2, "Recall by year")
    plotRecall, dataRecall = plotHBar2(recall2, "Recall by year")


    def onChangeRecallDate():
        print(begin.value)
        print(end.value)
        bV = begin.value
        eV = end.value

        bVStr = bV.strftime('%Y%m%d')
        eVStr = eV.strftime('%Y%m%d')

        print(bVStr)
        print(eVStr)

        data = recallByYear(fromDate=bVStr, toDate=eVStr)

        # print(data['x'])
        # print(data['y'])

        trueX = []
        trueY = []

        for i in range(0, len(data['x'])):
            year = data['x'][i][0:4]
            # print(year)
            if (year in trueX):
                idx = trueX.index(year)
            else:
                trueX.append(year)
                idx = trueX.index(year)

            if (len(trueY) < idx + 1):
                trueY.append(1)
            else:
                trueY[idx] = trueY[idx] + 1

        data2 = {'x': trueX, 'y': trueY}

        print(data2['x'])
        print(data2['y'])

        plotRecall.y_range.factors = data2['x']
        dataRecall.data['right'] = data2['y']

        dataRecall.data['y'] = list(range(1, len(data2['x']) + 1))
        print(dataRecall.data['y'])
        print(dataRecall.data['right'])


    begin = DatePicker(title="Begin Date:", min_date=datetime(2004, 1, 1),
                       max_date=datetime.now(),
                       value=datetime(datetime.now().year, 1, 1))

    end = DatePicker(title="End Date:", min_date=datetime(2004, 1, 1),
                     max_date=datetime.now(),
                     value=datetime(datetime.now().year, 1, 1))

    recallButton = Button(label="Show", button_type="success")
    recallButton.on_click(onChangeRecallDate)

    desc = Div(
        text="OpenFDA: Food recall enforcement reports. Recalls are and appropriate alternative method for removing or correcting "
             "marketed consumer products, their labeling, and/or promotional literature that violate the laws administred "
             "by the Food and Drug Administration (FDA).", width=800)

    draw([begin, end, recallButton], desc, plotRecall)
