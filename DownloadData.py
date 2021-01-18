from zeep import Client
import csv

client = Client("https://tools.rki.de/SurvStat/SurvStatWebService.svc?wsdl")

factory = client.type_factory("ns2")


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
            "ColumnHierarchy": "[AlterPerson80].[AgeGroupName6]",
            #AgeGroupName6 : 0,05,10,...,70,75,80+
            #AgeGroupName8 : 0,1,2,3,...,78,79,80+
        }
    )
    AgeGroups = [i["Caption"] for i in res.Columns.QueryResultColumn]
    YearWeek = [items.Caption for items in res.QueryResults.QueryResultRow]
    Data = [[item for item in items.Values.string] for items in res.QueryResults.QueryResultRow]

    #print(AgeGroups)
    #print(YearWeek)
    #print(Data)
    return AgeGroups, YearWeek, Data


def formatAgeGroup(AgeGroup):
    if isinstance(AgeGroup, list):
        return [formatAgeGroup(i) for i in AgeGroup]
    if '..' in AgeGroup:
        start, stop = AgeGroup[1:].split('..')
        if start == stop:
            return start
        else:
            return start + '-' + stop
    if AgeGroup == 'A80+':
        return '80+'
    return AgeGroup


def saveCSV():
    AgeGroups, YearWeek, Data = fetch()
    Data = Data[1:] # Remove Total over time
    # Data = Data[1:] # Remove Total over Age Groups
    # AgeGroups = AgeGroups[1:]
    YearWeek = YearWeek[1:]

    new_Age = formatAgeGroup(AgeGroups)
    YearWeek.insert(0,'Altergruppe')
    new_Data = list(zip(*Data[::1]))
    new_Data = [list(i) for i in new_Data]
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

saveCSV()