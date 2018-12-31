import pandas as pd
from pathlib import Path
import os
import json
import MerchantClassifier as mc

data = pd.read_csv("~/Developer//python/data/transactions.csv", header=0)

print("Imported data from csv file")

data['Date'] = data['Date'].astype('datetime64[ns]')
data['Labels'] = data['Labels'].astype(str)
data['Notes'] = data['Notes'].astype(str)

data.loc[data['Transaction Type'] == "credit", 'Amount'] *= -1

print("Converted the data types of Date, Label and Notes to datetime, str and str")

cc_data = data.loc[(data['Account Name'] != "RAJAGOPALAN PADMANABAN ANAND")
                & (data['Account Name'] != "RAJAGOPALAN PADMANABAN ANAND AISHWARYA KRISHNAMOHAN")
                & (data['Account Name'] != "TOTAL CHECKING")
                & (data['Account Name'] != "ONLINE SAVINGS")
                & (~((data['Original Description'].str.contains("THANK YOU")) & (data['Transaction Type'] == "credit")))
                & (~((data['Original Description'].str.contains("AUTOMATIC PAYMENT")) & (data['Transaction Type'] == "credit")))
                & (~((data['Original Description'].str.contains("BA ELECTRONIC PAYMENT")) & (data['Transaction Type'] == "credit")))
                & (~((data['Original Description'].str.contains("Payment Received")) & (data['Transaction Type'] == "credit")))]

print("Filtered for only credit card accounts")


cc_data_nov = cc_data[(cc_data['Date'] > "10/31/2018") & (cc_data['Date'] < "11/15/2018")]

print('Filtered for Nov 2018')



data_store = None
response = None
with open(Path(os.path.expanduser("~")+"/Documents/FinanceData/merchant_classification.json")) as classification_file:
    data_store = json.load(classification_file)
    print(data_store)
    response = mc.classify(cc_data_nov, data_store)

with open(Path(os.path.expanduser("~") + "/Documents/FinanceData/merchant_classification.json"), 'w') as updated_classification:
    json.dump(response[1], updated_classification)


response[0].to_csv("/Users/Raja/Documents/PersonalFinance/transactions/sample.csv")