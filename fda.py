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
    q = dateQuery
    genderNum = 0
    print(gender)
    if gender and gender != "All":
        if gender == "Male":
            genderNum = 1
        else:
            genderNum = 2
        q = q + "+AND+patient.patientsex:"+str(genderNum)
    else:
        q = q + "+AND+patient.patientsex:[1+TO+2]"

    req =  "/drug/event.json?search=" + q + '&count=patient.reaction.reactionmeddrapt.exact&limit=10'
    conn.request("GET", req)

    r1 = conn.getresponse()
    response = json.loads(r1.read().decode('utf-8'))

    barData = countToBarData(response["results"], "term", "count")
    print(req)
    print(barData['x'])
    print(barData['y'])

    dateQuery += "+AND+("
    i = 1
    for term in barData['x']:
        dateQuery = dateQuery + "patient.reaction.reactionmeddrapt.exact:%s" % urllib.parse.quote(term)  + "+OR+"

    dateQuery = dateQuery[:-4]
    dateQuery += ")"

    q = dateQuery
    if genderNum != 0:
        print("ALL query")
        q = q + "+AND+patient.patientsex:[1+TO+2]"
        req = "/drug/event.json?search=" + q + '&count=patient.reaction.reactionmeddrapt.exact'
        print(req)
        conn.request("GET", req)
        r1 = conn.getresponse()
        response = json.loads(r1.read().decode('utf-8'))
        barData['All'] = addBarData(barData, countToBarData(response["results"], "term", "count"))
    else:
        barData['All'] = barData['y']


    q = dateQuery
    if genderNum != 1:
        print("Male query")
        q = q + "+AND+patient.patientsex:1"
        req = "/drug/event.json?search=" + q + '&count=patient.reaction.reactionmeddrapt.exact'
        print(req)
        conn.request("GET", req)
        r2 = conn.getresponse()
        response = json.loads(r2.read().decode('utf-8'))
        barData['Male'] = addBarData(barData, countToBarData(response["results"], "term", "count"))
    else:
        barData['Male'] = barData['y']



    q = dateQuery
    if genderNum != 2:
        print("Female query")
        q = q + "+AND+patient.patientsex:2"
        req = "/drug/event.json?search=" + q + '&count=patient.reaction.reactionmeddrapt.exact'
        print(req)
        conn.request("GET", req)
        r3 = conn.getresponse()
        response = json.loads(r3.read().decode('utf-8'))
        barData['Female'] = addBarData(barData, countToBarData(response["results"], "term", "count"))
    else:
        barData['Female'] = barData['y']


    return barData

def addBarData(barData, newBarData):
    newY = [0] * len(barData['x'])

    i = 0
    for x in newBarData['x']:
        if x in barData['x']:
            yi = barData['x'].index(x)
            newY[yi] = newBarData['y'][i]
        i += 1

    print(barData['x'])
    print(newY)

    return newY

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
    conn.request("GET", "https://api.fda.gov/drug/event.json?search=receivedate:[20040101+TO+20161230]&count=patient.drug.medicinalproduct.exact&limit=10")
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


# https://open.fda.gov/food/enforcement/
# https://api.fda.gov/food/enforcement.json?count=state&limit=?
def productionCities(top=10):
    query = "/food/enforcement.json?count=state&limit=%s" % (top)

    conn.request("GET", query)

    r1 = conn.getresponse()
    response = json.loads(r1.read().decode('utf-8'))

    conn.close()
    return countToBarData(response["results"], "term", "count")


# https://open.fda.gov/food/enforcement/
# https://api.fda.gov/food/enforcement.json?search=recall_initiation_date:[20150101+TO+20171231]&count=recall_initiation_date
def recallByYear(fromDate='20150101', toDate='20171231'):
    query = "recall_initiation_date:[%s+TO+%s]&count=recall_initiation_date" % (fromDate, toDate)

    print(query)
    conn.request("GET", "/food/enforcement.json?search=" + query)
    r1 = conn.getresponse()

    if r1.getcode() >= 400:
        conn.close()
        return 0

    response = json.loads(r1.read().decode('utf-8'))

    conn.close()

    return countToBarData(response["results"], "time", "count")

def countToBarData(countResults, xName, yName):
    x = list(map(lambda result: result[xName], countResults))
    y = list(map(lambda result: result[yName], countResults))

    return {'x': x, 'y': y}