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

"""
Los productos que salen del registro civil son:
31
"""

import pandas as pd
import glob
import numpy as np
from  utils import *
import requests
import datetime as dt
import io

def normalizeRegCivDF(df):
    # rename columns
    df.rename(columns={'REGION': 'Region', 'COMUNA': 'Comuna'}, inplace=True)
    # title case => Title Case
    df['Comuna'] = df['Comuna'].str.title()
    regionNameRegex(df)
    regionName(df)

    # zero pad fechas
    df['MES'] = df['MES'].astype(str).apply(lambda x: x.zfill(2))
    df['DIA'] = df['DIA'].astype(str).apply(lambda x: x.zfill(2))
    # standard fecha
    df["Fecha"] = df["AÑO"].astype(str) + '-' + df["MES"].astype(str) + '-' + df["DIA"].astype(str)
    df = df.drop(columns={'AÑO', 'MES', 'DIA'})
    # handle duplicates
    df['TOTAL'] = df.groupby(['Region', 'Comuna', 'Fecha'])['TOTAL'].transform('sum')
    df.drop_duplicates(inplace=True)
    return df


def prod31_32(fte, prod):
    data = []
    outputPrefix = ''

    if 'producto31' in prod:
        outputPrefix = 'Nacimientos'
        for file in glob.glob(fte + 'Nacimientos/*.xlsx'):
            df = pd.read_excel(file)
            #rename columns
            df.rename(columns={'REGION': 'Region', 'COMUNA': 'Comuna'}, inplace=True)
            #title case => Title Case
            df['Comuna'] = df['Comuna'].str.title()
            regionNameRegex(df)
            regionName(df)

            # zero pad fechas
            df['MES'] = df['MES'].astype(str).apply(lambda x: x.zfill(2))
            df['DIA'] = df['DIA'].astype(str).apply(lambda x: x.zfill(2))
            # standard fecha
            df["Fecha"] = df["AÑO"].astype(str) + '-' + df["MES"].astype(str) + '-' + df["DIA"].astype(str)
            df = df.drop(columns={'AÑO', 'MES', 'DIA'})
            # handle duplicates
            df['TOTAL'] = df.groupby(['Region', 'Comuna', 'Fecha'])['TOTAL'].transform('sum')
            df.drop_duplicates(inplace=True)


            if 'Nacimientos' in file:
                df = df.rename(columns={'TOTAL': 'Nacimientos'})
                data.append(df)


    if 'producto32' in prod:
        outputPrefix = 'Defunciones'
        for file in glob.glob(fte + 'Defunciones/*.xlsx'):
            df = pd.read_excel(file)
            # rename columns
            df.rename(columns={'REGION': 'Region', 'COMUNA': 'Comuna'}, inplace=True)
            # title case => Title Case
            df['Comuna'] = df['Comuna'].str.title()
            regionNameRegex(df)
            regionName(df)

            # zero pad fechas
            df['MES'] = df['MES'].astype(str).apply(lambda x: x.zfill(2))
            df['DIA'] = df['DIA'].astype(str).apply(lambda x: x.zfill(2))
            # standard fecha
            df["Fecha"] = df["AÑO"].astype(str) + '-' + df["MES"].astype(str) + '-' + df["DIA"].astype(str)
            df = df.drop(columns={'AÑO', 'MES', 'DIA'})
            # handle duplicates
            df['TOTAL'] = df.groupby(['Region', 'Comuna', 'Fecha'])['TOTAL'].transform('sum')
            df.drop_duplicates(inplace=True)

            if 'Defunciones' in file:
                df = df.rename(columns={'TOTAL': 'Defunciones'})
                data.append(df)

    data = pd.concat(data)

    #Custom sort
    data['Region'] = pd.Categorical(data['Region'],
                                    ["Arica y Parinacota",
                                    "Tarapacá",
                                     "Antofagasta",
                                     "Atacama",
                                     "Coquimbo",
                                     "Valparaíso",
                                     "Metropolitana",
                                     "O’Higgins",
                                     "Maule",
                                     "Ñuble",
                                     "Biobío",
                                     "Araucanía",
                                     "Los Ríos",
                                     "Los Lagos",
                                     "Aysén",
                                     "Magallanes",
                                    ])

    data.to_csv(prod + outputPrefix + '_std.csv', index=False)


    reshaped = pd.pivot_table(data, index=['Region', 'Comuna'], columns=['Fecha'], values=outputPrefix)
    reshaped.fillna(0, inplace=True)
    reshaped = reshaped.applymap(np.int64)
    reshaped.to_csv(prod + outputPrefix + '.csv')

    data_t = reshaped.transpose()

    data_t.index.rename('', inplace=True)

    data_t.to_csv(prod + outputPrefix + '_T.csv')

def APIupdate(URL, prod):
    # check if we're on nacimientos or defunciones and when was the last update to the files
    suffix = ''
    outputPrefix = ''
    if 'producto31' in prod:
        print('Actualizando el producto 31')
        suffix = 'nacimiento'
        outputPrefix = 'Nacimientos'
        fileName = prod + 'Nacimientos_std.csv'
    elif 'producto32' in prod:
        print('Actualizando el producto 32')
        suffix = 'defuncion'
        outputPrefix = 'Defunciones'
        fileName = prod + 'Defunciones_std.csv'

    df = pd.read_csv(fileName, dtype={'Codigo region': object, 'Codigo Comuna': object, 'Fecha': str})

    # should add 1 day after max fecha to avoid duplications
    lastDate = max(df['Fecha'])

    lastDate_as_date = dt.datetime.strptime(lastDate, "%Y-%m-%d")
    lastDate = lastDate_as_date + dt.timedelta(days=1)
    lastDate = dt.datetime.strftime(lastDate, "%Y-%m-%d")
    now = dt.datetime.today().strftime("%Y-%m-%d")
    now_as_date = dt.datetime.strptime(now, "%Y-%m-%d")



    if (lastDate_as_date >= now_as_date):
        print("Todo esta actualizado. No hacemos nada")
        return 0

    else:
        # registro civil inserts retroactively. So we must drop a subset of the table to make sure we're up to date
        days_to_check = 14
        retroactiveDate_as_date = now_as_date - dt.timedelta(days=days_to_check)
        retroactiveDate = dt.datetime.strftime(retroactiveDate_as_date, "%Y-%m-%d")
        print("Dropping data after " + retroactiveDate)

        df_toKeep = df[df['Fecha'] < retroactiveDate]
        df_toDrop = df[df['Fecha'] >= retroactiveDate]
        print(len(df_toKeep))
        print(len(df_toDrop))
        print(len(df))
        df = df[df.Fecha < retroactiveDate]
        print(len(df))

        # get the xlsx from the API
        headers = {
            'Content-Type': 'application/json',
            'Origin': URL.replace('/api/estadistica/', ''),
            'Connection': 'keep-alive',
        }
        myData = {
            "startdate": retroactiveDate,
            "enddate": now
        }
        call = URL + suffix + '/getXlsxAllComunas'
        response = requests.post(call, headers=headers, json=myData)
        xlsx = io.BytesIO(response.content)

        # load the API to a DF
        df2 = pd.read_excel(xlsx)
        df2 = normalizeRegCivDF(df2)
        if 'nacimiento' in suffix:
            df2.rename(columns={'TOTAL': 'Nacimientos'}, inplace=True)

        elif 'defuncion' in suffix:
            df2.rename(columns={'TOTAL': 'Defunciones'}, inplace=True)

        data = []
        data.append(df)
        data.append(df2)
        data = pd.concat(data)

        # Custom sort
        data['Region'] = pd.Categorical(data['Region'],
                                        ["Arica y Parinacota",
                                         "Tarapacá",
                                         "Antofagasta",
                                         "Atacama",
                                         "Coquimbo",
                                         "Valparaíso",
                                         "Metropolitana",
                                         "O’Higgins",
                                         "Maule",
                                         "Ñuble",
                                         "Biobío",
                                         "Araucanía",
                                         "Los Ríos",
                                         "Los Lagos",
                                         "Aysén",
                                         "Magallanes",
                                         ])

        # normalize all on data, but test on df as it's smaller
        dfaux = insertCodigoRegion(data)
        if 'Nacimientos' in data.columns:
            # Region,Comuna,Nacimientos,Fecha,Código Región,Nombre Región,Código Provincia,Nombre Provincia,Código Comuna 2017,Nombre Comuna
            data = dfaux[['Nombre Región', 'Código Región', 'Nombre Comuna', 'Código Comuna 2017', 'Nacimientos', 'Fecha']].copy()

        elif 'Defunciones' in data.columns:
            data = dfaux[['Nombre Región', 'Código Región', 'Nombre Comuna', 'Código Comuna 2017', 'Defunciones', 'Fecha']].copy()

        data.rename(columns={'Nombre Región': 'Region',
                                 'Código Región': 'Codigo region',
                                 'Nombre Comuna': 'Comuna',
                                 'Código Comuna 2017': 'Codigo comuna'}, inplace=True)

        data.to_csv(prod + outputPrefix + '_std.csv', index=False)

        reshaped = pd.pivot_table(data, index=['Region', 'Codigo region', 'Comuna', 'Codigo comuna'], columns=['Fecha'], values=outputPrefix)
        reshaped.fillna(0, inplace=True)
        reshaped = reshaped.applymap(np.int64)
        reshaped.to_csv(prod + outputPrefix + '.csv')

        data_t = reshaped.transpose()

        data_t.index.rename('', inplace=True)

        data_t.to_csv(prod + outputPrefix + '_T.csv')

if __name__ == '__main__':
    bulk = False

    if bulk:
        # hay que obtener los xls a mano para generar en bulk.
        print('Generando el producto 31')
        prod31_32('../input/RegistroCivil/', '../output/producto31/')

        print('Generando el producto 32')
        prod31_32('../input/RegistroCivil/', '../output/producto32/')
    else:
        URL = 'https://api.sed.srcei.cl/api/estadistica/'

        APIupdate(URL, '../output/producto31/')

        APIupdate(URL, '../output/producto32/')
