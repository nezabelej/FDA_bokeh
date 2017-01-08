import http.client, urllib, ssl
import json
import pandas as pd

ssl._create_default_https_context = ssl._create_unverified_context
conn = http.client.HTTPSConnection("api.fda.gov")

#drug/event.json
params = urllib.parse.urlencode({
    'api_key': 'VLyIUAm6qwh0WMxMucGuLKSNl3YNNtvsyj78MjrX',
    'search': 'receivedate:[20040101+TO+20081231]',
    'limit': 1
})

#https://api.fda.gov/drug/event.json?search=receivedate:[20040101+TO+20170106]&count=patient.reaction.reactionmeddrapt.exact
def frequentAdverseReactions(fromDate='20040101', toDate='20170107'):
    dateQuery = "receivedate:[%s+TO+%s]" % (fromDate, toDate)

    conn.request("GET", "/drug/event.json?search=" + dateQuery + '&count=patient.reaction.reactionmeddrapt.exact')
    r1 = conn.getresponse()

    response = json.loads(r1.read().decode('utf-8'))

    conn.close()


    return countToBarData(response["results"], "Adverse reactions", "term", "count")




def countToBarData(countResults, dataName, xName, yName):
    transformed = {}
    i = 0
    for result in countResults:
        transformed[result[xName]] = result[yName]
        i += 1
        if i == 20:
            break

    return pd.DataFrame({dataName: transformed})