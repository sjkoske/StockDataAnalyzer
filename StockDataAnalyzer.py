## import regular expressions for format validation
import re
from datetime import datetime
## imported requests, must do "pip install requests on local machine for this to work"
import requests




## Prompting the user for Stock Symbol and Checking for correct formatting

def main():
   
    stock = GetStockName()
    chartType = GetChartType()
    timeSeries = GetTimeSeries()
    print("Enter StartDate (YYYY-MM-DD): ")
    startDate= GetDate()
    print("Enter End Date (YYYY-MM-DD): ")
    endDate = GetDate()

    # example code retrieving data from api
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=',stock,'&interval=5min&apikey=67ZV81HC5LKYSLBY'
    r = requests.get(url)
    data = r.json()
    print(data)



    

   
## Getting Stock name from user 
def GetStockName():
     while True:
        try:
            stock = input("Enter the Stock Symbol you want to use (up to five letters):  ").upper()
            if ((stock.isalpha() == True) & ((len(stock) > 0 ) & (len(stock) < 6))):
                print("The stock you have chosen is: ",stock)
                break
            else:
                print("Input was not in the correct format, try again.\n")
        except ValueError:
            print("incorrect value type\n")
            continue
     return stock



## Getting chart type from user
def GetChartType():
    
    while True:
        try: 
            chartType = int(input("Choose the chart type: \n1. Bar\n2. Line\n"))
            if (chartType == 1  or chartType == 2):
                break
            else:
                print("Please enter either 1 or 2.\n")
                continue
        except ValueError:
            print("Incorrect value type\n")
            continue
    return chartType

## Getting time series from user
def GetTimeSeries():
    while True:
        try: 
            timeSeries = int(input("Select the time series of the chart you wish to generate: \n1. Intraday\n2. Daily\n3. Weekly\n4. Monthly\n"))
            if (timeSeries == 1  or timeSeries == 2 or timeSeries == 3 or timeSeries == 4):
                break
            else:
                print("Please enter 1, 2, 3, or 4.\n")
                continue
        except ValueError:
            print("Incorrect value type\n")
            continue
    return timeSeries


## Getting Date input from user 
def GetDate():
    while True:
        date = input()
        if (ValidateDate(date) == True):
            break
        else:
            print("Enter your date in the correct format (YYYY-MM-DD).\n ")
    return date



## Validate that the date entered is in correct format
## IMPROVE REG EXPRESSION TO ONLY USE REAL DATES THAT ARE NOT FUTURE DATES 
def ValidateDate(date):
    regex = re.compile("[0-9]{4}\-[0-9]{2}\-[0-9]{2}")
    match = re.match(regex, date)
    if (match):
        return True
    else:
        return False


    
    
    
main()