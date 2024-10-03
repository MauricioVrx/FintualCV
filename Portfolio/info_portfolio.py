import numpy_financial as npf
import numpy as np
import pandas as pd
from datetime import datetime as dt, timedelta as td

def set_decimals(n, d = 2):
    return np.round(n,d)

indx = ["TIR", "Cuartil-1", "Mediana", "Cuartil-3", "Min", "Max", "Promedio", "Desv-Estandar"]  
file_excel = "precios.xlsx"


class Portfolio:
    '''
    En Fintual, un portafolio es una combinación de instrumentos financieros en los que se invierte tu dinero, ajustada a un nivel de riesgo y 
    retorno que se alinea con tus objetivos de inversión. Cada portafolio está diseñado con una estrategia específica que incluye una mezcla 
    de activos como bonos, acciones internacionales, y otros instrumentos, lo que permite diversificar la inversión y reducir el riesgo.
    
    __ini__ (sheet_name):

        Parameters
        ----------
        sheet_name : Str
            Nombre de la pestaña del archivo Excel de donde se obtendrá los datos del Portafolio
    '''

    def __init__(self, sheet_name, file_name = file_excel):
        self.name       = sheet_name                                           # Str       : Nombre del portafolio
        self.info       = pd.read_excel(f"{file_name}" ,sheet_name=sheet_name) # DataFrame : get_excel_info(sheet_name)
        self.primer_dia = self.info.iloc[-1]                                   # Series    : Datos del primer día historico del portafolio 
        self.ultimo_dia = self.info.iloc[ 0]                                   # Series    : Datos del último día del portafolio registrado en el documento
        self.anos       = self.info['ano'].unique().tolist()[::-1]             # list      : Listado de años transcurrido en el listado

        # Datos Precio del Portafolio de inicio a fin
        # Dataframe historico
        port_price = self.section_info(self.info, column_info_name="precio")

        # TIR
        self.t_tir      = port_price[0]
        # Cuartil 1
        self.t_cuatil1  = port_price[1]
        # Mediana
        self.t_mediana  = port_price[2]
        # Cuartil 3
        self.t_cuatil3  = port_price[3]
        # Min
        self.t_min      = port_price[4]
        # Max
        self.t_max      = port_price[5]
        # Promedio
        self.t_promedio = port_price[6]
        # Desviación estandar
        self.t_desv_std = port_price[7]


        # Dataframe con los datos estadisticos de "Precio" de la acción en el transcurso anual y mensual 
        self.t_price_year_info, self.t_price_months_info        = self.info_per_year(self.info, self.anos,months=True, column_info_name="precio")
        # Dataframe con los datos estadisticos de "Activos totales" de la acción en el transcurso anual y mensual
        self.t_total_assets_year_info, self.t_total_assets_months_info = self.info_per_year(self.info, self.anos,months=True, column_info_name="activos_totales")
        # Dataframe con los datos estadisticos de "Accionistas" de la acción en el transcurso anual y mensual
        self.t_shareholders_year_info, self.t_shareholders_months_info = self.info_per_year(self.info, self.anos,months=True, column_info_name="accionistas")
     

    def __str__(self):
        return self.name 

    def months_especific_info(self , df, value_name):
        return df.map(lambda x: x.get(value_name) if isinstance(x, dict) else None)
    
    # def get_months_especific_info(self, value_name):
    #     return RN_info.t_price_months_info.map(lambda x: x.get(value_name) if isinstance(x, dict) else None)

    def section_info(self, info, column_info_name="precio"):
        """Obtiene y calcula los valores estadisticos de inicio a fin de una columna en específico(Precio por defecto) del archivo de Excel 

        Parameters
        ----------
        info : Pandas DataFrame
            Dataframe con la información de Excel con los datos de la bolsa de inversión seleccionada 

        column_info_name : str , opcional
            Nombre de la columna del Dataframe a seleccionar, por defecto es "precio"

        Returns
        -------
        lista
            una lista con los valores principales de estadistica para el analisis de datos
        """
        po = info[[column_info_name]].to_numpy().squeeze()
            
        tir      = np.round(npf.irr([info.iloc[-1][column_info_name]*-1,info.iloc[0][column_info_name]])*100, decimals=2)
        cuatil1  = set_decimals(np.quantile(po, 0.25), 4)
        mediana  = set_decimals(np.quantile(po, 0.50), 4)
        cuatil3  = set_decimals(np.quantile(po, 0.75), 4)
        min      = np.rint(np.min(po))
        max      = np.rint(np.max(po))
        promedio = np.rint(np.average(po))
        desv_std = set_decimals(np.std(po),2)

        return [tir,cuatil1,mediana,cuatil3, min, max, promedio, desv_std ]


    def info_per_month(self, year_info, column_info_name="precio"):
        """ Funcion que permite adquirir los datos estadisticos a nivel mensual dentro del rango anual de un Dataframe 

        Parameters
        ----------
        year_info : Pandas DataFrame
            Dataframe con los datos anuales del protafolio

        column_info_name : str , opcional
            Nombre de la columna del Dataframe a seleccionar, por defecto es "precio"

        Returns
        -------
        Diccionario
            Diccionario que contiene el [año]: con otro diccionario que contiene los datos [estadísticos] 
        """

        tem_mensual = {}
        months_list =  year_info['mes'].unique().tolist()[::-1]
        for m in months_list:
            month_info = year_info[year_info['mes']==m]
            tem_mensual[m] = dict(zip(indx,self.section_info(month_info, column_info_name)))
        return tem_mensual


    def info_per_year(self, info, year_list, months=False, column_info_name="precio"):
        """ Funcion que permite adquirir los datos estadisticos a nivel anual dentro del rango total de un Dataframe 

        Parameters
        ----------
        year_list : lista
            listado de los años a que serán utilidazon en el iterable para los datos estadístico en el periodo de cada año

        months : Boolean
            En caso de ser 'True' tambien retornará la estadisticas a nivel menusal

        column_info_name : str , opcional
            Nombre de la columna del Dataframe a seleccionar, por defecto es "precio"
            
        Returns
        -------
        Dataframe
            DataFrame que contiene el [año]: con los datos [estadísticos] 
        
        Dataframe (Opcional)
            DataFrame que contiene el [mes]: con los datos [estadísticos] 
        
        """

        dict_anual   = {}
        dict_mensual = {}
        
        for y in year_list:
            year_info = info[info['ano']==y]
            dict_anual[y] = self.section_info(year_info, column_info_name)
            if months == True:
                dict_mensual[y] = self.info_per_month(year_info, column_info_name)
        
        df_anual  = pd.DataFrame(dict_anual, index=indx)

        if months == True:
            df_months = pd.DataFrame(dict_mensual)
            df_months = df_months.sort_index().T 
            return df_anual.T, df_months
        else:
            return df_anual.T
    

    def inf_between_2_dates(self, date1, date2, column_info_name="precio"):
        """ Función que entrega las estadistica entre dos fechas dadas(Rango inlusivo)

        Parameters
        ----------
        date1 : str
            Fecha inicial

        date2 : str
            Fecha final

        column_info_name : str , opcional
            Nombre de la columna del Dataframe a seleccionar, por defecto es "precio"
            
        Returns
        -------
        Dataframe
            Diccionario que contiene la [Fecha]: con  los datos [estadísticos] 
        """
        n1 = self.info.index[self.info['fecha'] == date1][0]
        n2 = self.info.index[self.info['fecha'] == date2][0]

        info_date_filter = self.info.iloc[n2: n1+1]

        return pd.DataFrame({f"{date1}/{date2}" : self.section_info(info_date_filter, column_info_name)}, index=indx)
        
    
    def info_per_month_from_date(self, original_date, months=1, column_info_name="precio"):
        """ Funcion que permite adquirir los datos estadisticos a nivel mensual dentro del rango anual de un Dataframe 

        Parameters
        ----------
        original_date : str
            Fecha inicial donde se calculará los meses

        months : int
            Cantidad de meses que se requiere obtener, cada mes corresponde a 30 días.
        
        column_info_name : str , opcional
            Nombre de la columna del Dataframe a seleccionar, por defecto es "precio"

        Returns
        -------
        Diccionario
            Diccionario que contiene el [año]: con otro diccionario que contiene los datos [estadísticos] 
        """
        parsed_date = dt.strptime(original_date, '%Y-%m-%d')
        li = []

        li.append(str(parsed_date)[:10])

        for i in range(1, months+1):
            li.append(str(parsed_date + td(days=30*i ))[:10])

        dt_per_month = pd.DataFrame(self.inf_between_2_dates(li[0], li[1], column_info_name))

        for i in range(1, len(li)-1):
            dt_per_month = dt_per_month.join(self.inf_between_2_dates(li[i], li[i+1], column_info_name))

        dt_per_month = dt_per_month.T

        return dt_per_month
    
def get_all_portfolios_info(file_name = file_excel):
    all_portfolios = {}
    xls = pd.read_excel(file_name,sheet_name=None)
    sheet_names = list(xls.keys())
    for p in sheet_names:
        tem_port = Portfolio(p)
        all_portfolios[tem_port.name] = tem_port
    
    return all_portfolios