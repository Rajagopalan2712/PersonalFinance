import pandas as pd
from pathlib import Path


def generate_data_frame(year: str):
    my_file = Path("~/Developer//python/data/"+year+".csv")
    if not my_file.is_file():
        return None
    data = pd.read_csv("~/Developer//python/data/"+year+".csv", header=0)
    return data


def load_and_generate_data_frame(data_source: str, year: str):
    print("loading data frame...")
    data_source_file = Path(data_source)
    if not data_source_file.is_file():
        return None
    data = pd.read_csv(data_source, header=0)
    data['Date'] = data['Date'].astype('datetime64[ns]')
    data['Labels'] = data['Labels'].astype(str)
    data['Notes'] = data['Notes'].astype(str)

    data.loc[data['Transaction Type'] == "credit", 'Amount'] *= -1

    print("Converted the data types of Date, Label and Notes to datetime, str and str")

    cc_data = data.loc[(data['Account Name'] != "RAJAGOPALAN PADMANABAN ANAND")
                       & (data['Account Name'] != "RAJAGOPALAN PADMANABAN ANAND AISHWARYA KRISHNAMOHAN")
                       & (data['Account Name'] != "TOTAL CHECKING")
                       & (data['Account Name'] != "ONLINE SAVINGS")
                       & (~(
                (data['Original Description'].str.contains("THANK YOU")) & (data['Transaction Type'] == "credit")))
                       & (~((data['Original Description'].str.contains("AUTOMATIC PAYMENT")) & (
                data['Transaction Type'] == "credit")))
                       & (~((data['Original Description'].str.contains("BA ELECTRONIC PAYMENT")) & (
                data['Transaction Type'] == "credit")))
                       & (~((data['Original Description'].str.contains("Payment Received")) & (
                data['Transaction Type'] == "credit")))]

    print("Filtered for only credit card accounts")
    data_filtered = data[(data['Date'] >= "01/01/"+year) & (cc_data['Date'] <= "12/31/"+year)]
    return data_filtered