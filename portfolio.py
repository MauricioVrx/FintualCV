import requests
from requests.structures import CaseInsensitiveDict
import numpy_financial as np
from datetime import datetime as dt

headers = CaseInsensitiveDict()
headers["accept"] = "application/json"

class Portfolio:
    __lastDayPrice = int
    __baseUrlApi = "https://fintual.cl/api/real_assets/"

    def __init__(self, id):
        urlAssetInfo     = f"{self.__baseUrlApi}{id}"
        assetInfo        = requests.get(urlAssetInfo,  headers=headers).json()['data']['attributes']
        urlAssetLastInfo = self.__baseUrlApi+str(id)+"/days?from_date="+str(assetInfo['last_day']['date'])+"&to_date="+str(assetInfo['last_day']['date'])
        assetLastInfo    = requests.get(urlAssetLastInfo,  headers=headers).json()['data'][0]['attributes']

        self.id          = id
        self.name        = assetInfo['name']
        self.startDate   = assetInfo['start_date']
        self.startPrice  = assetLastInfo['price']
        self.lastDate    = assetInfo['last_day']['date']
        self.lastPrice   = assetInfo['last_day']["net_asset_value"]


    # Get the price form a stock in specific day.
    def __oneDayPrice(self, date1, date2):
        dayInfo  = self.__baseUrlApi+str(self.id)+"/days?from_date="+str(date1)+"&to_date="+str(date2)
        dayPrice =  float(requests.get(dayInfo, headers=headers).json()['data'][0]['attributes']['price'])
        return dayPrice

    # if initial value exist previosly, this will by using at "iPrice" skiping the first call "__oneDayPrice" method
    def profitBetweenTwoDates(self, initialDate, lastDate, existInfo=False):
        if existInfo == False:
            iPrice = self.__oneDayPrice(initialDate,initialDate)
        else:
            iPrice = initialDate
        lPrice = self.__oneDayPrice(lastDate,lastDate)

        self.__lastDayPrice = lPrice

        profit = round(np.irr([-iPrice, lPrice])*100,2)
        return profit
    

    # Get the profit from the beggining to its last  day ussing "profitBetweenTwoDates" method.
    def profitAllTime(self):
        #*** MAKE HOURS VALIDATOR (if hour <=  19:00) ***#
        return self.profitBetweenTwoDates(self.startDate,self.lastDate)
    

    # Generate stock's profit for each year.
    def annualizedReturn(self):
        annualized_profit = {}
        date_format = "%Y/%m/%d"

        iDate = (self.startDate).replace("-","/")
        lDate = (self.lastDate ).replace("-","/")

        year1 =dt.date(dt.strptime(iDate,date_format)).year
        year2 =dt.date(dt.strptime(lDate,date_format)).year
        countYears = year2-year1

        if countYears == 0:
            annualized_profit[year1] = self.profitBetweenTwoDates(iDate,lDate)
        else:
            annualized_profit[year1] = self.profitBetweenTwoDates(iDate,str(year1)+"/12/31")
            if countYears > 1:
                for i in range (1, countYears):
                    annualized_profit[year1+i] = self.profitBetweenTwoDates(self.__lastDayPrice,str(year1+i)+"/12/31", True)
            annualized_profit[year2] = self.profitBetweenTwoDates(str(year2)+"/01/01",lDate)
        
        return annualized_profit


if __name__ == '__main__':
    myPortfolio = [186,187,188]

    print("\n")

    "Show portfolios from 'myPorfolio' list"
    for i in myPortfolio:
        portX = Portfolio(i)
        print(f"*** {portX.name} ***")
        print(f"- All time profit          : {portX.profitAllTime()}")
        print(f'- Profit between two dates : {portX.profitBetweenTwoDates("2019-10-15","2022-01-03")}')
        print(f"- Annualized profit        : ")
        for i, j in portX.annualizedReturn().items():
            print(f"\t{i}: {j}")
        print("\n\n")
