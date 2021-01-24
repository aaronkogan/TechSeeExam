#!/usr/bin/python3

import csv;
import math;

street=[];city=[];zipcode=[];state=[];beds=[];baths=[];sq__ft=[];typeflat=[];sale_date=[];price=[];latitude=[];longitude=[]

def loadCsv():
    with open('Sacramentorealestatetransactions.txt') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                #Read first line with Column names
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                street.append(row[0])
                city.append(row[1])
                zipcode.append(row[2])
                state.append(row[3])
                beds.append(row[4])
                baths.append(row[5])
                sq__ft.append(row[6])
                typeflat.append(row[7])
                sale_date.append(row[8])
                price.append(row[9])
                latitude.append(row[10])
                longitude.append(row[11])
                line_count += 1

def report():
    i = 0
    cName = []
    prices = []
    for cityName in city:
        if i == 0 :
            cName.append(cityName)
            prices.append([price[i]])
        else:
            if cityName in cName:
                prices[cName.index(cityName)].append(price[i])
            else:
                cName.append(cityName)
                prices.append([price[i]])
        i += 1
    f = open('report.txt', 'w')
    f.write('city,avg price per city,total price per city\n')
    i = 0
    for cityName in cName:
        prices_int = [int(x) for x in prices[i]]
        avg = math.trunc(sum(prices_int)/len(prices_int))
        f.write(cName[i]+',' + str(avg)+','+str(sum(prices_int))+'\n')
        i += 1
    f.close()

def additionalReport():
    i = 0
    fixPrice = ['0' for x in range(50)] # if square = 0 exept from total calculate price
    fixSquare = []
    cName = []
    prices = []
    raw_beds = []
    raw_square = []
    raw_dates = []
    firstSellYear = 0
    firstSellMonth = 0
    firstSellDay = 0
    lastSellYear = 0
    lastSellMonth = 0
    lastSellDay = 0
    nMonth = {
    'Jan': 1,
    'Feb': 2,
    'Mar': 3,
    'Apr': 4,
    'May': 5,
    'Jun': 6,
    'Jul': 7,
    'Aug': 8,
    'Sep': 9,
    'Oct': 10,
    'Nov': 11,
    'Dec': 12
    }

    for cityName in city:
        if i == 0:
            cName.append(cityName)
            prices.append([price[i]])
            raw_beds.append([beds[i]])
            raw_square.append([sq__ft[i]])
            raw_dates.append([sale_date[i]])
            if(int(sq__ft[i]) == 0):
                fixPrice[cName.index(cityName)] = price[i]
        else:
            if cityName in cName:
                prices[cName.index(cityName)].append(price[i])
                raw_beds[cName.index(cityName)].append(beds[i])
                raw_square[cName.index(cityName)].append(sq__ft[i])
                raw_dates[cName.index(cityName)].append(sale_date[i])
                if(int(sq__ft[i]) == 0):
                    fixPrice[cName.index(cityName)] = int(fixPrice[cName.index(cityName)]) + int(price[i])
            else:
                cName.append(cityName)
                prices.append([price[i]])
                raw_beds.append([beds[i]])
                raw_square.append([sq__ft[i]])
                raw_dates.append([sale_date[i]])
            if(int(sq__ft[i]) == 0):
                fixPrice[cName.index(cityName)] = price[i]
        i += 1
    f = open('additional_report.txt', 'w')
    f.write('city,avg beds number per city,avg square meter price,first sale date per city,last sale date per city\n')
    i = 0
    for cityName in cName:
        beds_int = [int(x) for x in raw_beds[i]]
        prices_int = [int(x) for x in prices[i]]
        square_int = [int(x) for x in raw_square[i]]
        avg_beds = math.trunc(sum(beds_int)/len(beds_int))
        if sum(square_int)!=0:    
            avg_price_ft = math.trunc((sum(prices_int)) - int(fixPrice[i]) / sum(square_int))
        j = 0
        while(j<len(raw_dates[i])):
            if j == 0:
                firstSellYear = int(raw_dates[i][j][-4:]) #get year in int
                lastSellYear = int(raw_dates[i][j][-4:])
                firstSellMonth = int(nMonth[raw_dates[i][j][4:7]]) #get month in int
                lastSellMonth = int(nMonth[raw_dates[i][j][4:7]])
                firstSellDay = int(raw_dates[i][j][8:10])
                lastSellDay = int(raw_dates[i][j][8:10])
            else:
                if firstSellYear > int(raw_dates[i][j][-4:]):
                    firstSellYear = int(raw_dates[i][j][-4:])
                if lastSellYear < int(raw_dates[i][j][-4:]):
                    lastSellYear = int(raw_dates[i][j][-4:])
                if firstSellMonth > int(nMonth[raw_dates[i][j][4:7]]):
                    firstSellMonth = int(nMonth[raw_dates[i][j][4:7]])
                if lastSellMonth < int(nMonth[raw_dates[i][j][4:7]]):
                    lastSellMonth = int(nMonth[raw_dates[i][j][4:7]])
                if firstSellDay > int(raw_dates[i][j][8:10]):
                    firstSellDay = int(raw_dates[i][j][8:10])
                if lastSellDay < int(raw_dates[i][j][8:10]):
                    lastSellDay = int(raw_dates[i][j][8:10])              
            j += 1
        f.write(cName[i]+',' + str(avg_beds)+',' +str(avg_price_ft)+',' +str(firstSellDay)+'/'+str(firstSellMonth)+'/'+str(firstSellYear)+',' +str(lastSellDay)+'/'+str(lastSellMonth)+'/'+str(lastSellYear)+'\n')
        i += 1
    f.close()

loadCsv()
report()
additionalReport()
