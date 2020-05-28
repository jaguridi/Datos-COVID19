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

import pandas as pd
import glob
import numpy as np
from utils import *
import requests
import datetime as dt
import io
import sys

"""
Los productos que salen del registro civil son:
31
"""



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
    df = normalizaNombreCodigoRegionYComuna(df)
    df.sort_values(by=['Codigo region', 'Codigo comuna', 'Fecha'], na_position='first', inplace=True)
    return df


def prod31_32(fte, prod):
    data = []
    outputPrefix = ''

    if 'producto31' in prod:
        outputPrefix = 'Nacimientos'
        for file in glob.glob(fte + 'Nacimientos/*.xlsx'):
            if '_DO' not in file:
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
            if '_DO' not in file:
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

    #Normalize and sort
    data = normalizaNombreCodigoRegionYComuna(data)
    data.sort_values(by=['Codigo region', 'Codigo comuna', 'Fecha'], inplace=True)

    data.to_csv(prod + outputPrefix + '_std.csv', index=False)

    reshaped = pd.pivot_table(data, index=['Region', 'Codigo region', 'Comuna', 'Codigo comuna'], columns=['Fecha'], values=outputPrefix)
    reshaped.fillna(0, inplace=True)
    reshaped = reshaped.applymap(np.int64)
    reshaped.to_csv(prod + outputPrefix + '.csv')

    data_t = reshaped.transpose()

    data_t.index.rename('', inplace=True)

    data_t.to_csv(prod + outputPrefix + '_T.csv')


def updateInputDO(fte, prod, fromDate='2020-01-01', toDate=dt.datetime.today().strftime("%Y-%m-%d")):
    # check if we're on nacimientos or defunciones and when was the last update to the files
    suffix = ''
    outputPrefix = ''
    if 'Nacimientos' in prod:
        print('Actualizando el producto 31')
        suffix = 'nacimiento'
        outputPrefix = 'Nacimientos'

    elif 'Defunciones' in prod:
        print('Actualizando el producto 32')
        suffix = 'defuncion'
        outputPrefix = 'Defunciones'


    # get the xlsx from the API
    headers = {
        'Content-Type': 'application/json',
        'Origin': fte.replace('/api/estadistica/', ''),
        'Connection': 'keep-alive',
    }
    myData = {
        "startdate": fromDate,
        "enddate": toDate
    }
    call = fte+ suffix + '/getXlsxAllComunas'
    print('Querying ' + call + ' between ' + fromDate + ' and ' + toDate)
    response = requests.post(call, headers=headers, json=myData)
    xlsx = io.BytesIO(response.content)

    # load the API to a DF
    df_API = pd.read_excel(xlsx)
    df_API = normalizeRegCivDF(df_API)

    # Normalize and sort
    df_API = normalizaNombreCodigoRegionYComuna(df_API)
    df_API.sort_values(by=['Codigo region', 'Codigo comuna', 'Fecha'], inplace=True)

    if 'nacimiento' in suffix:
        df_API.rename(columns={'TOTAL': 'Nacimientos'}, inplace=True)
    elif 'defuncion' in suffix:
        df_API.rename(columns={'TOTAL': 'Defunciones'}, inplace=True)

    fileName = prod + outputPrefix + '_' + fromDate + '_' + toDate + '_DO.csv'

    #check for duplicates:

    compareAPIAgainstFile(df_API, fromDate, toDate)

    df_API.to_csv(fileName, index=False)


def prod31_32DO(fte, prod):
    data = []
    outputPrefix = ''
    df_2020 = []
    if 'producto31' in prod:
        outputPrefix = 'Nacimientos'
        for file in glob.glob(fte + 'Nacimientos/*_DO.csv'):
            df = pd.read_csv(file)
            data.append(df)
            if '2020-01-01' in file:
                 df_2020 = df


    if 'producto32' in prod:
        outputPrefix = 'Defunciones'
        for file in glob.glob(fte + 'Defunciones/*_DO.csv'):
            df = pd.read_csv(file)
            data.append(df)
            if '2020-01-01' in file:
                 df_2020 = df

    data = pd.concat(data)
    data.to_csv(prod + outputPrefix + '_std.csv', index=False)

    reshaped = pd.pivot_table(data, index=['Region', 'Codigo region', 'Comuna', 'Codigo comuna'],
                              columns=['Fecha'], values=outputPrefix)
    reshaped.fillna(0, inplace=True)
    reshaped = reshaped.applymap(np.int64)
    reshaped.to_csv(prod + outputPrefix + '.csv')

    data_t = reshaped.transpose()
    data_t.index.rename('', inplace=True)
    data_t.to_csv(prod + outputPrefix + '_T.csv')

    # issue 223: light product to consume raw from gh
    df_2020.to_csv(prod + '2020-' + outputPrefix + '_std.csv', index=False)
    reshaped = pd.pivot_table(df_2020, index=['Region', 'Codigo region', 'Comuna', 'Codigo comuna'],
                              columns=['Fecha'],
                              values=outputPrefix)
    reshaped.fillna(0, inplace=True)
    reshaped = reshaped.applymap(np.int64)
    reshaped.to_csv(prod + '2020-' + outputPrefix + '.csv')
    data_t = reshaped.transpose()
    data_t.index.rename('', inplace=True)
    data_t.to_csv(prod + '2020-' + outputPrefix + '_T.csv')




def compareAPIAgainstFile(df_api, fromDate, toDate):
    '''
    We compare what's stored against what the API reply, and report those changes
    '''
    #La API nos dice que archivo abrir: lo inferimos a partir de la fecha

    df_file = pd.DataFrame()
    if 'Nacimientos' in list(df_api.columns):
        inputPrefix = 'Nacimientos'
        for file in glob.glob('../input/RegistroCivil/Nacimientos/Nacimientos_' + fromDate + '_' + toDate + '_DO.csv'):
            print('Reading ' + file + ' for comparison')
            df_file = pd.read_csv(file)


    if 'Defunciones' in list(df_api.columns):
        inputPrefix = 'Defunciones'
        for file in glob.glob('../input/RegistroCivil/Defunciones/Defunciones_' + fromDate + '_' + toDate + '_DO.csv'):
            df_file = pd.read_csv(file)

    if len(df_file) == 0:
        print('No file to compare')
        return

    # teoria: concatenar y hacer drop de duplicados

    if len(df_file) == 0:
        return

    print('largo file ' + str(len(df_file)) + ' + largo api ' + str(len(df_api)) + ' = '
          + str(len(df_file)+len(df_api)))

    #prepare to check for duplicates.
    # 1.- Concat both DF

    results = pd.concat([df_file, df_api])
    duplications = results[results.duplicated(['Codigo region', 'Codigo comuna', 'Fecha'])]
    print('concat the df gives ' + str(len(results)))
    results = results.reset_index(drop=True)
    results_gpby = results.groupby(list(df_file.columns))
    idx = [x[0] for x in results_gpby.groups.values() if len(x) !=1]
    results = results.reindex(idx)
    print(len(results))
    if len(results > 0):
        print('All data from the API was on disk. No changes')

    else:
        print('New data from the API.')
        print('We have ' + str(len(duplications)) + ' duplications')
        duplications['Fecha'] = pd.to_datetime(duplications['Fecha'])
        df_file['Fecha'] = pd.to_datetime(df_file['Fecha'])

        if (duplications['Fecha'] < max(df_file['Fecha'])).any():
            print('History changed. Notifying')
            # just write a tmp file which will be sent to s3 ( an we can evaluate if sent to slack only.
            timestamp = dt.datetime.today().strftime("%Y-%m-%dT%H:%M:%S")
            duplications.to_csv(fromDate + '-' + toDate + '-changes-on-' + inputPrefix + '-' + timestamp + '.tmp',
                           index=False)

def removeOldFiles():
    '''
    for 2020 we change filename every day, so for the change of day we must make sure we keep asingle file
    '''
    today_as_date = dt.datetime.today()
    today = today_as_date.strftime("%Y-%m-%d")
    yesterday_as_date = today_as_date - dt.timedelta(days=1)
    yesterday = yesterday_as_date.strftime("%Y-%m-%d")
    print(yesterday)
    if '2020' in today:
        print('Searching for files older than ' + today)
        for file in glob.glob('../input/RegistroCivil/*/*' + yesterday + '_DO.csv'):
            todays_file = file.replace(yesterday, today)
            print('Found ' + file + ' to delete. Doing only if there\'s a file for today')
            if os.path.isfile(todays_file):
                print('Found a file for today: ' + todays_file + '. Removing yesterday\'s')
                os.remove(file)



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

    #Normalize and sort
    df_API = normalizaNombreCodigoRegionYComuna(df_API)
    df_API.sort_values(by=['Codigo region', 'Codigo comuna', 'Fecha'], inplace=True)


    if 'nacimiento' in suffix:
        df_API.rename(columns={'TOTAL': 'Nacimientos'}, inplace=True)

    elif 'defuncion' in suffix:
        df_API.rename(columns={'TOTAL': 'Defunciones'}, inplace=True)




    #compare df with what was written:
    df_on_disk = pd.read_csv(prod + outputPrefix + '_std.csv')
    df_on_disk['Fecha'] = pd.to_datetime(df_on_disk['Fecha'])
    df_on_disk.sort_values(by=['Codigo region', 'Codigo comuna', 'Fecha'], inplace=True)
    #df_on_disk.drop_duplicates(subset=['Region', 'Codigo region', 'Comuna', 'Codigo comuna', 'Fecha'], keep='last', inplace=True)
    df_API['Fecha'] = pd.to_datetime(df_API['Fecha'])
    print('largo API')
    print(len(df_API))

    properFromDate = dt.datetime.strptime(fromDate, "%Y-%m-%d")
    properToDate = dt.datetime.strptime(toDate, "%Y-%m-%d")
    df_to_check = df_on_disk.loc[(df_on_disk['Fecha'] >= properFromDate) & (df_on_disk['Fecha'] <= properToDate)]

    df_to_check.sort_values(by=['Codigo region', 'Codigo comuna', 'Fecha'], inplace=True)
    df_to_check.drop_duplicates(subset=['Region', 'Codigo region', 'Comuna', 'Codigo comuna', 'Fecha'],
                                keep='last', inplace=True)
    print('largo disco')
    print(len(df_to_check))
    print(max(df_to_check['Fecha']))
    print(min(df_to_check['Fecha']))


    # https://stackoverflow.com/questions/20225110/comparing-two-dataframes-and-getting-the-differences
    aux = pd.concat([df_to_check, df_API])
    print(len(aux))
    aux.sort_values(by=['Codigo region', 'Codigo comuna', 'Fecha'], inplace=True)

    aux.drop_duplicates(subset=['Region', 'Codigo region', 'Comuna', 'Codigo comuna', 'Fecha'], keep='last', inplace=True)
    print(len(aux))

    now = dt.datetime.today().strftime("%Y-%m-%d")
    now_as_date = dt.datetime.strptime(now, "%Y-%m-%d")

    if aux.empty:
        #lo que hay en disco es igual a la API => no hubo cambios
        print('No changes found on the API records')
    else:
        print('Found ' + str(len(aux)) + ' changes. Updating disk')

        if (aux['Fecha'] < now_as_date).any():
            print('History changed. Notifying')
            # remove rows by dup and replace TOTAL
            df_on_disk = pd.concat([df_on_disk, aux])
            df_on_disk.drop_duplicates(subset=['Region', 'Codigo region', 'Comuna', 'Codigo comuna', 'Fecha'],
                                       keep='last', inplace=True)

            #print(changes.to_string()) #NOTIFY THIS
            timestamp = dt.datetime.today().strftime("%Y-%m-%dT%H:%M:%S")
            #aux.to_csv(fromDate + '-' + toDate + '-changes-on-' + suffix + '-' + timestamp + '.tmp', index=False)

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
            #updateHistoryFromAPI(URL, '../output/producto31/', fromDate=sys.argv[1], toDate=sys.argv[2])
            #updateHistoryFromAPI(URL, '../output/producto32/', fromDate=sys.argv[1], toDate=sys.argv[2])
            updateInputDO(URL, '../input/RegistroCivil/Nacimientos/', fromDate=sys.argv[1], toDate=sys.argv[2])
            updateInputDO(URL, '../input/RegistroCivil/Defunciones/', fromDate=sys.argv[1], toDate=sys.argv[2])
        elif len(sys.argv) == 1:
            print('Actualizando productos para el año 2020')
            #updateHistoryFromAPI(URL, '../output/producto31/')
            #updateHistoryFromAPI(URL, '../output/producto32/')
            updateInputDO(URL, '../input/RegistroCivil/Nacimientos/')
            updateInputDO(URL, '../input/RegistroCivil/Defunciones/')
        else:
            print('something\'s wrong with ' + str(len(sys.argv)) + ' arguments')

        print('Generando el producto 31')
        prod31_32DO('../input/RegistroCivil/', '../output/producto31/')
        print('Generando el producto 32')
        prod31_32DO('../input/RegistroCivil/', '../output/producto32/')
        removeOldFiles()
