import requests
from requests.structures import CaseInsensitiveDict
import numpy_financial as npf
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
        self.df          = self.get_all_days()
    
    def __str__(self):
        return self.name

    def get_all_days(self):
        urlAssetInfoDays     = f"{self.__baseUrlApi}{self.id}/days?to_date=2024-08-28" # Obtener la información desde el inicio hasta la fecha 2024-08-28
        # urlAssetInfoDays     = f"{self.__baseUrlApi}{self.id}/days"                    # Obtener la información desde el inicio hasta la actualidad
        assetInfoDays        = requests.get(urlAssetInfoDays,  headers=headers).json()['data']

        df = pd.DataFrame(assetInfoDays)

        df = pd.json_normalize(df['attributes'])[['date', 'price', 'shareholders', 'total_assets', 'total_net_assets', 'outstanding_shares']]

        df = df[1:-1]

        df.columns = ('fecha','precio','accionistas','activos_totales','activos_neto_totales','acciones_en_circulación')

        df['ano'] = df['fecha'].apply(lambda x: dt.strptime(x, "%Y-%m-%d").year)
        df['mes'] = df['fecha'].apply(lambda x: dt.strptime(x, "%Y-%m-%d").month)
        df['dia'] = df['fecha'].apply(lambda x: dt.strptime(x, "%Y-%m-%d").day)

        self.df = df[['fecha', 'ano', 'mes', 'dia', 'precio', 'accionistas', 'activos_totales', 'activos_neto_totales', 'acciones_en_circulación']]
        return self.df 
    
    def ordenar_bolsa(self):
        self.df = self.df [['fecha', 'ano', 'mes', 'dia', 'precio', 'accionistas', 'activos_totales', 'activos_neto_totales', 'acciones_en_circulación']]
        return self.df 
    

def make_excel_file(pt_list=[186,187,188]):
    li_port = []
    for n in pt_list:
        li_port.append(Portfolio(n))

    with pd.ExcelWriter("precios_c.xlsx") as writer:
        for port_n in li_port:
            port_n.df.to_excel(writer, sheet_name=f"{port_n.name}") 