'''
MIT License

Copyright (c) 2020 Sebastian Cornejo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
import requests
from bs4 import BeautifulSoup
from unidecode import unidecode

"""
Utilidades genéricas
"""
import pandas as pd
import re

def regionName(df):
    df["Region"] = df["Region"].replace({"Tarapaca": "Tarapacá", "Valparaiso": "Valparaíso",
                                         "Región Metropolitana de Santiago": "Metropolitana",
                                         "Del Libertador General Bernardo O’Higgins": "O’Higgins",
                                         "Libertador General Bernardo OHiggins": "O’Higgins",
                                         "Nuble": "Ñuble",
                                         "Biobio": "Biobío", "Concepción": "Biobío",
                                         "La Araucania": "Araucanía", "la Araucanía": "Araucanía",
                                         "Los Rios": "Los Ríos", "de Los Ríos": "Los Ríos",
                                         "Aysen": "Aysén", "Aysén del General Carlos Ibañez del Campo": "Aysén",
                                         "Magallanes y la Antartica": "Magallanes",
                                         "Magallanes y de la Antártica Chilena": "Magallanes"
                                         })

def regionNameRegex(df):
    df['Region'] = df['Region'].replace(regex=True, to_replace=r'.*Región de ', value=r'')
    df['Region'] = df['Region'].replace(regex=True, to_replace=r'.*Región del ', value=r'')

def normalizaNombreCodigoRegionYComuna(df):
    # standards:
    df["Comuna"] = df["Comuna"].replace({"Coyhaique": "coihaique",
                                         "Paihuano": "paiguano",
                                         "La Calera": "Calera",
                                         "Llay-Llay": "Llaillay",
                                         })

    # Lee IDs de comunas desde página web oficial de SUBDERE
    df_dim_comunas = pd.read_excel("http://www.subdere.gov.cl/sites/default/files/documentos/cut_2018_v03.xls",
                                   encoding="utf-8")

    # Crea columna sin tildes, para hacer merge con datos publicados
    #df_dim_comunas["Comuna"] = df_dim_comunas["Nombre Comuna"].str.normalize("NFKD").str.encode("ascii", errors="ignore").str.decode("utf-8")
    df_dim_comunas["Comuna"] = df_dim_comunas["Nombre Comuna"].str.normalize("NFKD")\
        .str.encode("ascii", errors="ignore").str.decode("utf-8").str.lower().str.replace(' ', '')


    df["Comuna"] = df["Comuna"].str.normalize("NFKD").str.encode("ascii", errors="ignore").str.decode("utf-8")\
        .str.lower().str.replace(' ', '')

    #df = df.merge(df_dim_comunas, on="Comuna", how="outer")
    df = df.merge(df_dim_comunas, on="Comuna", how="inner")

    df['Comuna'] = df['Nombre Comuna']
    df['Codigo comuna'] = df['Código Comuna 2017']
    df['Region'] = df['Nombre Región']
    df['Codigo region'] = df['Código Región']

    df.drop(columns={'Código Región','Nombre Región',
                     'Código Comuna 2017', 'Nombre Comuna',
                     'Código Provincia', 'Nombre Provincia'
                     }, inplace=True)

    # Sort Columns
    columnsAddedHere = ['Region', 'Codigo region', 'Comuna', 'Codigo comuna']
    originalColumns = [x for x in list(df) if x not in columnsAddedHere]
    sortedColumns = columnsAddedHere + originalColumns

    #report on missing
    df1 = df[df.isnull().any(axis=1)]
    if df1.size > 0:
        print(df1.to_string())

    df = df[sortedColumns]
    df['Codigo region'] = df['Codigo region'].astype(str)
    return df

def FechaAlFinal(df):
    if 'Fecha' in df.columns:
        columns = [x for x in list(df) if x != 'Fecha']
        columns.append('Fecha')
        df = df[columns]
        return df
    else:
        print('No hay una columna Fecha en tu dataframe')


def transpone_csv(csvfile):
    df = pd.read_csv(csvfile)
    return(df.T)


def std_getSuperficieComunas(URL):
    '''
    Obtenemos la superficie de las comunas desde Wikipedia, y las dejamos en un archivo en input para
    enriquecer los productos
    '''
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find(lambda tag: tag.name == 'table')
    rows = table.findAll(lambda tag: tag.name == 'tr')
    data = [['Codigo comuna', 'Comuna', 'Escudo', 'Provincia', 'Region', 'Superficie_km2', 'Poblacion_2017', 'Densidad',
            'IDH_2005', 'IDH_2005_b', 'Latitud', 'Longitud']]
    for row in rows:
        cols = row.findAll('td')
        cols = [ele.text.strip() for ele in cols]
        if len(cols) > 1:
            data.append(
                #s.replace('.', '', s.count('.')-1)
                [unidecode(ele.replace('.', '', ele.count('.')-1)) for ele in cols if (len(ele) > 1 or 'Escudo' not in ele)])

    headers = data.pop(0) # gives the headers as list and leaves d
    df = pd.DataFrame.from_records(data, columns=headers)

    df_to_write = df.drop(columns=['Provincia', 'Region', 'Poblacion_2017', 'Densidad',
            'IDH_2005', 'IDH_2005_b', 'Latitud', 'Longitud', 'Escudo'])

    # standards:
    df_to_write["Comuna"] = df_to_write["Comuna"].replace({"La Calera": "Calera", "Llay-Llay": "Llaillay"})
    df_to_write = normalizaNombreCodigoRegionYComuna(df_to_write)


    return df_to_write


def std_getPoblacion(fte, std_df):
    '''
    Agregamos poblacion a input/Otros/InformacionComunas.csv
    '''
    df = pd.read_csv(fte)
    # standards:
    df["Comuna"] = df["Comuna"].replace({"OHiggins": "O'Higgins"})
    df = normalizaNombreCodigoRegionYComuna(df)

    columnsToKeep = ['Codigo comuna', 'Poblacion']
    df = df[columnsToKeep]

    # if there is a poblacion columns, drop it
    if 'Poblacion' in std_df:
        std_df = std_df.drop(columns=['Poblacion'])

    columnsToKeep = list(std_df)
    columnsToKeep.append('Poblacion')
    std_df = std_df.merge(df, on="Codigo comuna", how="outer")
    return std_df


def writeStandardsToFile(prod):
    '''
    Actualizamos y/o generamos el archivo con entradas mas estables para las comunas:
    Region,Codigo region,Comuna,Codigo comuna,Superficie_km2,Poblacion
    '''
    out = std_getSuperficieComunas('https://es.wikipedia.org/wiki/Anexo:Comunas_de_Chile')
    out = std_getPoblacion('../output/producto1/Covid-19.csv', out)
    out.to_csv(prod, index=False)


def insertSuperficiePoblacion(df):
    df_std = pd.read_csv('../input/Otros/InformacionComunas.csv')
    df_sup = df_std[['Codigo comuna', 'Superficie_km2', 'Poblacion']]
    df = df.merge(df_sup, on="Codigo comuna", how="outer")

    # Sort Columns
    columnsAddedHere = ['Superficie_km2', 'Poblacion']
    originalColumns = [x for x in list(df) if x not in columnsAddedHere]
    sortedColumns = columnsAddedHere + originalColumns

    df = df[sortedColumns]

    return df


if __name__ == '__main__':
    writeStandardsToFile('../input/Otros/InformacionComunas.csv')