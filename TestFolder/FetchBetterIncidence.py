# https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_COVID19/FeatureServer/0/query?where=1%3D1&outFields=Meldedatum,NeuerFall,NeuerTodesfall&outSR=4326&f=json
# API Link

# https://impfdashboard.de/static/data/germany_vaccinations_timeseries_v2.tsv
# Impf-Daten
import json
import urllib.request
import numpy as np
import matplotlib.pyplot as plt
import datetime
import pickle, io
import pandas as pd

def save_obj(obj, name ):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)



def countData(dicti,date,value,count):
    date = str(date)
    value = str(value)
    def add2dict_dict(dicti,value):
        if value not in dicti:
            dicti[value] = dict()
        #return dicti
    def add2dict(dicti,value,count):
        if value not in dicti:
            dicti[value] = count
        else:
            dicti[value] += count
        #return dicti
    add2dict_dict(dicti, date)
    add2dict(dicti[date], value,count)
    #return dicti


def get_cases(dicti, date):
    plus = minus = null = 0
    try:
        minus = -dicti[date]['-1']
    except:
        None
    try:
        plus = dicti[date]['1']
    except:
        None
    try:
        null = dicti[date]['0']
    except:
        None
    return null, plus, minus

"""
time_case_dict = dict()
time_death_dict = dict()
notFinished = True
offset = 0#1000000

while notFinished:
    with urllib.request.urlopen("https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_COVID19/"
                            "FeatureServer/0/query?where=1%3D1&outFields=Meldedatum,Refdatum,AnzahlFall,AnzahlTodesfall,NeuerFall,NeuerTodesfall&"
                            "outSR=4326&"+"resultOffset={:}".format(offset)+"&f=json") as url:
        data = json.loads(url.read().decode())
        if 'exceededTransferLimit' not in data:
            notFinished = False
        offset = offset+len(data['features'])
        print(offset)
        #if offset > 10000:
        #    notFinished = False
        for it in data['features']: # alternativ statt Meldedatum: Refdatum
            countData(time_case_dict, int(it['attributes']['Refdatum']/1000), it['attributes']['NeuerFall'],it['attributes']['AnzahlFall'])
            countData(time_death_dict, int(it['attributes']['Refdatum']/1000), it['attributes']['NeuerTodesfall'],it['attributes']['AnzahlTodesfall'])
save_obj(time_case_dict, 'case')
save_obj(time_death_dict, 'death')

time_case_dict = load_obj('case')
time_death_dict = load_obj('death')

time_array = np.array(list(time_case_dict.keys()), dtype=int)
time_array.sort()
case_list = np.zeros((3,len(time_array)))
death_list = np.zeros((3,len(time_array)))
time_list = []
for i, item in enumerate(time_array):
    case_list[0, i], case_list[1, i], case_list[-1, i] = get_cases(time_case_dict,str(item))
    time_list.append(datetime.date.fromtimestamp(item))


plt.plot(time_list, np.convolve(case_list[0]+case_list[1]+case_list[-1],[1,1,1,1,1,1,1],'same')/83000000*100000,label='Inzidenz')
plt.plot(time_list, (case_list[0]+case_list[1]+case_list[-1])/83000000*100000*7,label='0')
#plt.plot(time_list, case_list[0],label='0')
#plt.plot(time_list, case_list[1],label='1')
#plt.plot(time_list, case_list[-1],label='-1')
plt.legend()
plt.show()

print(time_list, time_death_dict)
#"""
with urllib.request.urlopen('https://impfdashboard.de/static/data/germany_vaccinations_timeseries_v2.tsv') as url:
    c = pd.read_table(io.StringIO(url.read().decode()))
    c.date = pd.to_datetime(c.date,format='%Y-%m-%d')
    #print(c.date)
    print(c.columns.values.tolist())
    for col in ['dosen_kumulativ','dosen_differenz_zum_vortag', 'dosen_erst_differenz_zum_vortag', 'dosen_zweit_differenz_zum_vortag', 'personen_erst_kumulativ', 'personen_voll_kumulativ', 'impf_quote_erst', 'impf_quote_voll']:#c.columns.values.tolist():
        if col=='date':
            continue
        plt.plot(c['date'], c[col], label=col)
    plt.legend()
    plt.show()