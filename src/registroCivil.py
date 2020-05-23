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
import os
import sys

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

        # issue 223: light product to consume raw from gh
        df_2020 = data[data['Fecha'] >= '2020-01-01']
        df_2020.to_csv(prod + '2020-' + outputPrefix + '_std.csv', index=False)
        reshaped = pd.pivot_table(df_2020, index=['Region', 'Codigo region', 'Comuna', 'Codigo comuna'], columns=['Fecha'], values=outputPrefix)
        reshaped.fillna(0, inplace=True)
        reshaped = reshaped.applymap(np.int64)
        reshaped.to_csv(prod + '2020-' + outputPrefix + '.csv')
        data_t = reshaped.transpose()
        data_t.index.rename('', inplace=True)
        data_t.to_csv(prod + '2020-' + outputPrefix + '_T.csv')


def updateHistoryFromAPI(fte, prod, fromDate='2020-01-01', toDate=dt.datetime.today().strftime("%Y-%m-%d")):
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

    # get the xlsx from the API
    headers = {
        'Content-Type': 'application/json',
        'Origin': URL.replace('/api/estadistica/', ''),
        'Connection': 'keep-alive',
    }
    myData = {
        "startdate": fromDate,
        "enddate": toDate
    }
    call = URL + suffix + '/getXlsxAllComunas'
    print('Querying ' + call + ' between ' + fromDate + ' and ' + toDate)
    response = requests.post(call, headers=headers, json=myData)
    xlsx = io.BytesIO(response.content)

    # load the API to a DF
    df_API = pd.read_excel(xlsx)
    df_API = normalizeRegCivDF(df_API)

    if 'nacimiento' in suffix:
        df_API.rename(columns={'TOTAL': 'Nacimientos'}, inplace=True)

    elif 'defuncion' in suffix:
        df_API.rename(columns={'TOTAL': 'Defunciones'}, inplace=True)

    df_API['Region'] = pd.Categorical(df_API['Region'],
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
    dfaux = insertCodigoRegion(df_API)
    if 'Nacimientos' in df_API.columns:
        # Region,Comuna,Nacimientos,Fecha,Código Región,Nombre Región,Código Provincia,Nombre Provincia,Código Comuna 2017,Nombre Comuna
        df_API = dfaux[
            ['Nombre Región', 'Código Región', 'Nombre Comuna', 'Código Comuna 2017', 'Nacimientos', 'Fecha']].copy()

    elif 'Defunciones' in df_API.columns:
        df_API = dfaux[
            ['Nombre Región', 'Código Región', 'Nombre Comuna', 'Código Comuna 2017', 'Defunciones', 'Fecha']].copy()

    df_API.rename(columns={'Nombre Región': 'Region',
                         'Código Región': 'Codigo region',
                         'Nombre Comuna': 'Comuna',
                         'Código Comuna 2017': 'Codigo comuna'}, inplace=True)


    #compare df with what was written:
    df_on_disk = pd.read_csv(prod + outputPrefix + '_std.csv')
    df_on_disk['Fecha'] = pd.to_datetime(df_on_disk['Fecha'])
    df_API['Fecha'] = pd.to_datetime(df_API['Fecha'])

    properFromDate = dt.datetime.strptime(fromDate, "%Y-%m-%d")
    properToDate = dt.datetime.strptime(toDate, "%Y-%m-%d")
    df_to_check = df_on_disk.loc[(df_on_disk['Fecha'] >= properFromDate) & (df_on_disk['Fecha'] <= properToDate)]

    # https://stackoverflow.com/questions/20225110/comparing-two-dataframes-and-getting-the-differences
    aux = pd.concat([df_to_check, df_API])
    aux = aux.reset_index(drop=True)
    aux_gpby = aux.groupby(list(aux.columns))
    idx = [x[0] for x in aux_gpby.groups.values() if len(x) == 1]
    changes = aux.reindex(idx)
    changes.drop_duplicates(['Region', 'Codigo region', 'Comuna', 'Codigo comuna', 'Fecha'], keep='last', inplace=True)
    #print(list(changes))

    now = dt.datetime.today().strftime("%Y-%m-%d")
    now_as_date = dt.datetime.strptime(now, "%Y-%m-%d")

    if changes.empty:
        print('No changes found on the API records')
    else:
        print('Found changes. Updating disk')

        if (changes['Fecha'] < now_as_date).any():
            print('History changed. Notifying')
            # remove rows by dup and replace TOTAL
            df_on_disk = pd.concat([df_on_disk, changes])
            df_on_disk.drop_duplicates(['Region', 'Codigo region', 'Comuna', 'Codigo comuna', 'Fecha'],
                                                       keep='last', inplace=True)
            print(changes.to_string()) #NOTIFY THIS
            timestamp = dt.datetime.today().strftime("%Y-%m-%dT%H:%M:%S")
            changes.to_csv(fromDate + '-' + toDate + '-changes-on-' + suffix + '-' + timestamp + '.tmp', index=False)


        else:

            print('Just new records found. Appending')
            df_on_disk = pd.concat([df_on_disk, df_API])
            df_on_disk.drop_duplicates(['Region', 'Codigo region', 'Comuna', 'Codigo comuna', 'Fecha'],
                                       keep='last', inplace=True)


        df_on_disk.to_csv(prod + outputPrefix + '_std.csv', index=False)

        reshaped = pd.pivot_table(df_on_disk, index=['Region', 'Codigo region', 'Comuna', 'Codigo comuna'], columns=['Fecha'],
                                  values=outputPrefix)
        reshaped.fillna(0, inplace=True)
        reshaped = reshaped.applymap(np.int64)
        reshaped.to_csv(prod + outputPrefix + '.csv')

        data_t = reshaped.transpose()

        data_t.index.rename('', inplace=True)

        data_t.to_csv(prod + outputPrefix + '_T.csv')

        # issue 223: light product to consume raw from gh
        if '2020' in fromDate:
            df_2020 = df_on_disk[df_on_disk['Fecha'] >= '2020-01-01']
            df_2020.to_csv(prod + '2020-' + outputPrefix + '_std.csv', index=False)
            reshaped = pd.pivot_table(df_2020, index=['Region', 'Codigo region', 'Comuna', 'Codigo comuna'], columns=['Fecha'],
                                      values=outputPrefix)
            reshaped.fillna(0, inplace=True)
            reshaped = reshaped.applymap(np.int64)
            reshaped.to_csv(prod + '2020-' + outputPrefix + '.csv')
            data_t = reshaped.transpose()
            data_t.index.rename('', inplace=True)
            data_t.to_csv(prod + '2020-' + outputPrefix + '_T.csv')


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
        if len(sys.argv) == 3:
            print('Actualizando productos entre ' + sys.argv[1] + ' y ' + sys.argv[2])
            updateHistoryFromAPI(URL, '../output/producto31/', fromDate=sys.argv[1], toDate=sys.argv[2])
            updateHistoryFromAPI(URL, '../output/producto32/', fromDate=sys.argv[1], toDate=sys.argv[2])
        elif len(sys.argv) == 1:
            print('Actualizando productos para el año 2020')
            updateHistoryFromAPI(URL, '../output/producto31/')
            updateHistoryFromAPI(URL, '../output/producto32/')
        else:
            print('something\'s wrong with ' + str(len(sys.argv)) + ' arguments')

        #APIupdate(URL, '../output/producto31/')

        #APIupdate(URL, '../output/producto32/')
