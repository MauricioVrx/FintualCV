import requests
from requests.structures import CaseInsensitiveDict
import numpy_financial as np
from datetime import datetime as dt
import pandas as pd

headers = CaseInsensitiveDict()
headers["accept"] = "application/json"


class Portfolio:
    __baseUrlApi = "https://fintual.cl/api/real_assets/"

    def __init__(self, id):
        urlAssetInfo         = f"{self.__baseUrlApi}{id}"
        assetInfo            = requests.get(urlAssetInfo,  headers=headers).json()['data']['attributes']
        
        self.id          = id
        self.name        = assetInfo['name']
        self.startDate   = assetInfo['start_date']
        self.lastDate    = assetInfo['last_day']['date']
        self.lastPrice   = assetInfo['last_day']["net_asset_value"]
        self.df          = pd.DataFrame() 

    def get_all_days(self):
        '''Función que permite extraer todos los datos diarios de "asset" en formato DataFrame'''
        urlAssetInfoDays     = f"{self.__baseUrlApi}{self.id}/days"
        assetInfoDays        = requests.get(urlAssetInfoDays,  headers=headers).json()['data']

        df = pd.DataFrame(assetInfoDays)

        df = pd.json_normalize(df['attributes'])[['date', 'price', 'shareholders', 'total_assets', 'total_net_assets', 'outstanding_shares']]

        # if dt.now().hour < 19:
        df = df[1:]

        df.columns = ('fecha','precio','accionistas','activos_totales','activos_neto_totales','acciones_en_circulación')

        self.df = df
        return self.df 
    

if __name__ == '__main__':
    # Listado de real_assets principales
    # myPortfolio = [186,187,188, 15077]

    port15077 = Portfolio(15077)
    port15077.get_all_days()
    dt15077 = port15077.df

    port186 = Portfolio(186)
    port186.get_all_days()
    dt186 = port186.df

    port187 = Portfolio(187)
    port187.get_all_days()
    dt187 = port187.df

    port188 = Portfolio(188)
    port188.get_all_days()
    dt188 = port188.df

    # Se Crea el archivo excel de los datos de los 'assets' principales en distintas pestañas
    with pd.ExcelWriter("precios.xlsx") as writer:
        dt15077.to_excel(writer, sheet_name=f"{port15077.name}")  
        dt186.to_excel(writer, sheet_name=f"{port186.name}")  
        dt187.to_excel(writer, sheet_name=f"{port187.name}")  
        dt188.to_excel(writer, sheet_name=f"{port188.name}") 