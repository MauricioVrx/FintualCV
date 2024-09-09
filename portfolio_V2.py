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
        urlAssetInfoDays     = f"{self.__baseUrlApi}{self.id}/days"
        assetInfoDays        = requests.get(urlAssetInfoDays,  headers=headers).json()['data']

        df = pd.DataFrame(assetInfoDays)

        df = pd.json_normalize(df['attributes'])[['date', 'price', 'shareholders', 'total_assets', 'total_net_assets', 'outstanding_shares']]

        # if dt.now().hour < 19:
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
    

def make_excel_file():
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


  

if __name__ == '__main__':
    # Listado de real_assets principales
    # myPortfolio = [186,187,188, 15077]

    # información del Desarrollo de contrato
    info = pd.read_excel(f"precios.xlsx")

    # Diccionario donde se guardarán los datos importantes Wdel documento
    datos_excel = {}

    # Aislamos la primera columna para encontrar algunas palabras claves 
    # primera_col = info.iloc[:,0]

    # Buscamos la posición del campo "Contrato" dentro de la primera columna del documento. 
    # Esta indice nos permitirá encontrar los otros datos  
    # indice_contrato = info.index[primera_col == 'Contrato:'][0]
    print(info)

    