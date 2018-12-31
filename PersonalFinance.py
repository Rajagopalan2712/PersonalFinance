import DataFrameGenerator as dfg
from pathlib import Path
import os
import json
import pandas as pd
import MerchantClassifier as mc

def get_date_range(year:str, month:str):
    year_int = int(year)
    month_int = int(month)
    start_date=month+"/01/"+year
    last_day_of_month=None
    if month_int == 2 and year % 4 == 0:
        last_day_of_month = "29"
    elif month_int == 2:
        last_day_of_month = "28"
    elif month_int in [1,3,5,7,8,10,12]:
        last_day_of_month = "31"
    else:
        last_day_of_month = "30"

    end_date = month+"/"+last_day_of_month+"/"+year

    return start_date, end_date

reportYear = input("Enter the year : ")
reportMonth = input("Enter the month : ")
data = dfg.generate_data_frame(reportYear)
if data is None:
    dataSource = input("Enter path to transactions file : ")
    data = dfg.load_and_generate_data_frame(dataSource, reportYear)

data_store = None
response = None
with open(Path(os.path.expanduser("~")+"/Documents/FinanceData/merchant_classification.json")) as classification_file:
    data_store = json.load(classification_file)
    print(data_store)
    response = mc.classify(data, data_store)

with open(Path(os.path.expanduser("~") + "/Documents/FinanceData/merchant_classification.json"), 'w') as updated_classification:
    json.dump(response[1], updated_classification)

response[0].to_csv("/Users/Raja/Documents/PersonalFinance/transactions/"+reportYear+".csv")

report_date_range = get_date_range(reportYear, reportMonth)

print("Filtered for date range "+report_date_range[0] +" to "+ report_date_range[1])

data_for_report = response[0][(response[0]['Date'] >= report_date_range[0]) & (response[0]['Date'] <= report_date_range[1])]


print(data_for_report.groupby(['Labels']).sum())
print(data_for_report.groupby(['Labels', 'Description']).sum())


