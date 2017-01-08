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


#https://api.fda.gov/food/event.json?count=products.industry_name.exact
#https://api.fda.gov/food/event.json?search=outcomes:"serious+injuries"&count=products.industry_name.exact
    #search = outcomes:"serious+injuries"
#https://api.fda.gov/food/event.json?search=reactions:alopecia&count=products.industry_name.exact
    #search = reactions:alopecia
def typesOfReportedProducts(search=''):
    query='?'
    if search:
        query='?search='+search+'&'

    print("/drug/event.json" + query + '?count=products.industry_name.exact')
    conn.request("GET", "/food/event.json" + query + 'count=products.industry_name.exact')

    r1 = conn.getresponse()
    response = json.loads(r1.read().decode('utf-8'))

    conn.close()
    return countToBarData(response["results"], "term", "count")

def countToBarData(countResults, dataName, xName, yName):
    transformed = {}
    i = 0
    for result in countResults:
        transformed[result[xName]] = result[yName]
        i += 1
        if i == 20:
            break

    return pd.DataFrame({dataName: transformed})