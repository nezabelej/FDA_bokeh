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
def frequentAdverseReactions(fromDate='20040101', toDate='20170107', gender=''):
    dateQuery = "receivedate:[%s+TO+%s]" % (fromDate, toDate)

    if gender and gender != "All":
        if gender == "Male":
            genderNum = 1
        else:
            genderNum = 2
        dateQuery = dateQuery+"+AND+patient.patientsex:"+str(genderNum)

    conn.request("GET", "/drug/event.json?search=" + dateQuery + '&count=patient.reaction.reactionmeddrapt.exact&limit=10')
    r1 = conn.getresponse()

    response = json.loads(r1.read().decode('utf-8'))

    conn.close()


    return countToBarData(response["results"], "term", "count")


#https://api.fda.gov/drug/event.json?search=receivedate:[20040101+TO+20170106]+AND+patient.drug.medicinalproduct:ROCEPHIN+AND+patient.drug.medicinalproduct:PYOSTACINE (PRISTINAMYCIN)
def countReactionsInCombination(drugindication1, drugindication2):
    conn.request("GET", "https://api.fda.gov/drug/event.json?search=receivedate:[20040101+TO+20170106]+AND+patient.drug.medicinalproduct:"+drugindication1
                 +"+AND+patient.drug.medicinalproduct:"+drugindication2)

    #encode url, da bodo delali oklepaji

    r1 = conn.getresponse()

    if r1.getcode() >= 400:
        conn.close()
        return 0

    response = json.loads(r1.read().decode('utf-8'))
    conn.close()

    return response["meta"]["results"]["total"]

#https://api.fda.gov/food/event.json?count=products.industry_name.exact
#https://api.fda.gov/food/event.json?search=outcomes:"serious+injuries"&count=products.industry_name.exact
    #search = outcomes:"serious+injuries"
#https://api.fda.gov/food/event.json?search=reactions:alopecia&count=products.industry_name.exact
    #search = reactions:alopecia
def typesOfReportedProducts(search=''):
    query='?'
    if search:
        if (search == 'serious'):
            search = 'outcomes:"serious+injuries"'
        elif (search == 'hairLoss'):
            search = 'reactions:alopecia'
        query='?search='+search+'&'

    conn.request("GET", "/food/event.json" + query + 'count=products.industry_name.exact&limit=10')

    r1 = conn.getresponse()

    response = json.loads(r1.read().decode('utf-8'))

    conn.close()
    return countToBarData(response["results"], "term", "count")


def frequentDrugs():
    conn.request("GET", "https://api.fda.gov/drug/event.json?search=receivedate:[20040101+TO+20161230]&count=patient.drug.medicinalproduct.exact&limit=5")
    r1 = conn.getresponse()
    response = json.loads(r1.read().decode('utf-8'))
    conn.close()

    return list(map(lambda result: result["term"], response["results"]))

#https://open.fda.gov/food/event/
#https://api.fda.gov/food/event.json?count=date_created
def dateOfCreatedReport():
    conn.request("GET", "/food/event.json?count=date_created")

    r1 = conn.getresponse()
    response = json.loads(r1.read().decode('utf-8'))

    conn.close()
    return countToBarData(response["results"], "time", "count")



def countToBarData(countResults, xName, yName):
    x = list(map(lambda result: result[xName], countResults))
    y = list(map(lambda result: result[yName], countResults))

    return {'x': x, 'y': y}