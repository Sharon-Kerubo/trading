import csv
import os
from itrader.models import StockData

def run():
    file = open('C:/Trading Application/trading/data/stock_data.csv')
    read_file = csv.reader(file)

    StockData.objects.all().delete()

    count = 1

    for record in read_file:
        if count==1:
            pass
        else: 
            print(record)
            StockData.objects.create(security=record[0],lastprice=int(float(record[1])),demandqty=int(record[2]),demandprice=int(float(record[3])),supplyprice=int(float(record[4])),supplyqty=int(record[5]),lastqty=int(record[6]),high=int(float(record[7])),low=int(float(record[8])))
        count = count+1