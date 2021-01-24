from zeep import Client
import datetime
import csv
import numpy as np
import re
client = Client("https://tools.rki.de/SurvStat/SurvStatWebService.svc?wsdl")

factory = client.type_factory("ns2")



def formatAgeGroup(AgeGroup):
    if isinstance(AgeGroup, list):
        return [formatAgeGroup(i) for i in AgeGroup]
    if '..' in AgeGroup:
        start, stop = AgeGroup[1:].split('..')
        if start == stop:
            return start
        else:
            return start + '-' + stop

    if AgeGroup.find('+') != -1: # == 'A80+':
        return AgeGroup[1:]
    return AgeGroup



def clean_fetch(remove_unknown = True):
    def fetch():
        res = client.service.GetOlapData(
            {
                "Language": "German",
                "Measures": {"Count": 0},
                "Cube": "SurvStat",
                "IncludeTotalColumn": False,
                "IncludeTotalRow": False,
                "IncludeNullRows": False,
                "IncludeNullColumns": False,
                "HierarchyFilters": factory.FilterCollection(
                    [
                        {
                            "Key": {
                                "DimensionId": "[PathogenOut].[KategorieNz]",
                                "HierarchyId": "[PathogenOut].[KategorieNz].[Krankheit DE]",
                            },
                            "Value": factory.FilterMemberCollection(
                                ["[PathogenOut].[KategorieNz].[Krankheit DE].&[COVID-19]"]
                            ),
                        }
                    ]
                ),
                "RowHierarchy": "[ReportingDate].[YearWeek]",
                "ColumnHierarchy": "[AlterPerson80].[AgeGroupName2]",
                # AgeGroupName1 : ['Gesamt' '00' '01' '02' '03' '04' '05-09' '10-14' '15-19' '20-24' '25-29' '30-39' '40-49' '50-59' '60-69' '70-79' '80+']
                # AgeGroupName2 : ['Gesamt' '00-04' '05-09' '10-14' '15-19' '20-24' '25-29' '30-39' '40-49' '50-59' '60-69' '70-79' '80+']
                # AgeGroupName3 : ['Gesamt' '00-14' '15-19' '20-24' '25-29' '30-39' '40-49' '50-59' '60-69' '70-79' '80+']
                # AgeGroupName4 : ['Gesamt' '00-14' '15+']
                # AgeGroupName5 : ['Gesamt' '00-14' '15-59' '60+']
                # AgeGroupName6 : ['Gesamt' '00-04' '05-09' '10-14' '15-19' '20-24' '25-29' '30-34' '35-39' '40-44' '45-49' '50-54' '55-59' '60-64' '65-69' '70-74' '75-79' '80+']
                # AgeGroupName7 : ['Gesamt' '00-01' '02-04' '05-19' '20-39' '40-59' '60-79' '80+']
                # AgeGroupName8 : 0,1,2,3,...,78,79,80+
                # AgeGroupName9 : ['Gesamt' '00-01' '02-09' '10-19' '20-39' '40-59' '60-79' '80+']
                #10 : ['Gesamt' '00-14' '15-39' '40+']
            }
        )
        AgeGroups = [i["Caption"] for i in res.Columns.QueryResultColumn]
        YearWeek = [items.Caption for items in res.QueryResults.QueryResultRow]
        Data = [[item for item in items.Values.string] for items in res.QueryResults.QueryResultRow]
        return AgeGroups, YearWeek, Data

    AgeGroups, YearWeek, Data = fetch()
    Data = Data[1:]  # Remove Total over time
    # Data = Data[1:] # Remove Total over Age Groups
    # AgeGroups = AgeGroups[1:]
    YearWeek = np.array(YearWeek[1:])

    new_Age = np.array(formatAgeGroup(AgeGroups))
    #YearWeek.insert(0, 'Altergruppe')
    new_Data = list(zip(*Data[::1]))
    new_Data = np.array([list(i) for i in new_Data])
    if remove_unknown:
        new_Data = new_Data[new_Age != 'Unbekannt']
        new_Age = new_Age[new_Age != 'Unbekannt']
    new_Data[new_Data==None]=0
    new_Data = new_Data.astype(np.int)
    return new_Age, YearWeek, new_Data

def incidence():
    AgeGroups, YearWeek, Data = clean_fetch()
    age_num = count_age(AgeGroups)
    for i in range(len(age_num)):
        Data[i] = Data[i]/age_num[i]*100000
    return AgeGroups, YearWeek, Data

def count_age(age_bracket):
    if isinstance(age_bracket, (list, np.ndarray)):
        return [count_age(age) for age in age_bracket]
    def get_count(age,plus=False):
        age_count = [774870, 794132, 802415, 807816, 782143, 771479, 743954, 741969, 725807, 743761, 732376, 751663,
                     746670, 731698, 740506, 756823, 757882, 771938, 798514, 854086, 878869, 905902, 947646, 944591,
                     931423, 947032, 978142, 995515, 1030314, 1123468, 1109227, 1133582, 1109010, 1088700, 1055201,
                     1048086, 1048762, 1069168, 1059479, 1063715, 1011818, 997428, 987623, 968885, 943272, 954462,
                     960829, 1038797, 1139590, 1179680, 1263945, 1320960, 1352770, 1385608, 1386952, 1408832, 1392942,
                     1344388, 1319852, 1271291, 1230109, 1157125, 1124758, 1087957, 1047822, 1021046, 981186, 972595,
                     946118, 938087, 898100, 811462, 754507, 648189, 561837, 740528, 740375, 704285, 836403, 854829,
                     814346, 726011, 643708, 585337, 524879, 2386854, 83166711]
        if age == 'Gesamt':
            return age_count[-1]
        if plus:
            return np.sum(age_count[age:-1])
        return age_count[age]
    if age_bracket == 'Unbekannt':
        return -1
    age_list = re.split(r'[\+\-]',age_bracket)
    age_list = [age for age in age_list if age != '']
    if age_list[0]=='Gesamt':
        return get_count(-1)
    if len(age_list)==1:
        if age_bracket.find('+')!=-1:
            return get_count(int(age_list[0]), True)
        return get_count(int(age_list[0]))
    else:
        return np.sum([get_count(i) for i in range(int(age_list[0]),int(age_list[1])+1)])

def yw2datetime(yw):
    if isinstance(yw, (list, np.ndarray)):
        return [yw2datetime(i) for i in yw]
    yw_int = [int(i) for i in yw.split('-KW')]
    weekday = datetime.datetime(yw_int[0], 1, 1).weekday()
    if weekday <= 3:  # Thursday
        date_diff = 1 - weekday
    else:
        date_diff = 8 - weekday
    if date_diff > 0:
        return datetime.datetime(yw_int[0], 1, date_diff) + datetime.timedelta(weeks=yw_int[1] - 1, days=6)
    else:
        return datetime.datetime(yw_int[0] - 1, 12, 31 + date_diff) + datetime.timedelta(weeks=yw_int[1] - 1, days=6)

def extrapolateLastWeek(YearWeek, Data):
    week_diff = (yw2datetime(YearWeek[-1])+datetime.timedelta(hours=24)-datetime.datetime.now())/datetime.timedelta(weeks=1)

    if 0 < week_diff < 1:
        def extrap_function(value,w_diff):
            distr = [0, 0.1040, 0.2656, 0.4730, 0.6555, 0.8019, 0.9283, 1.0000]
            # the distribution is based on the reportet cases per weekday in germany from 22.01.2020 to 23.01.2021
            return value/np.interp(1-w_diff,np.linspace(0,1,len(distr)),distr)
        for i in range(len(Data)):
            Data[i][-1] = extrap_function(Data[i][-1],week_diff)
        return Data, True
    return Data, False



def saveCSV():
    new_Age, YearWeek, new_Data = clean_fetch()
    YearWeek.insert(0,'Altergruppe')
    #print(new_Data)
    for i in range(len(new_Data)):
        new_Data[i].insert(0, new_Age[i])
    #print(new_Data)
    #print(list(zip(Data)))
    with open('currentData.csv', 'wt', newline ='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(i for i in YearWeek)
        #writer.writerow(i for i in YearWeek)

        for j in new_Data:
            writer.writerow(j)

#saveCSV()