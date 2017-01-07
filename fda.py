import httplib, urllib, ssl
import json
import pandas as pd

ssl._create_default_https_context = ssl._create_unverified_context
conn = httplib.HTTPSConnection("api.fda.gov")

#drug/event.json
params = urllib.urlencode({
    'api_key': 'VLyIUAm6qwh0WMxMucGuLKSNl3YNNtvsyj78MjrX',
    'search': 'receivedate:[20040101+TO+20081231]',
    'limit': 1
})

#https://api.fda.gov/drug/event.json?search=receivedate:[20040101+TO+20170106]&count=patient.reaction.reactionmeddrapt.exact
def frequentAdverseReactions(fromDate='20040101', toDate='20170107'):
    dateQuery = "receivedate:[%s+TO+%s]" % (fromDate, toDate)

    conn.request("GET", "/drug/event.json?search=" + dateQuery + '&count=patient.reaction.reactionmeddrapt.exact')
    r1 = conn.getresponse()

    response = json.loads(r1.read())

    conn.close()


    return countToBarData(response["results"], "term", "count")




def countToBarData(countResults, xName, yName):
    x = list(map(lambda result: result[xName], countResults))
    y = list(map(lambda result: result[yName], countResults))

    return {'x': x, 'y': y}
    #return pd.DataFrame({xName: x, yName: y})