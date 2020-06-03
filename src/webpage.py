'''
MIT License

Copyright (c) 2020 Sebastian Cornejo, Miguel Angel Bustos

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
Los productos que salen de la pagina web del minsal son:
5
11
"""


import requests
from bs4 import BeautifulSoup
import csv
import unidecode
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

import utils

def get_minsal_page(minsalURL):
    page = requests.get(minsalURL)
    soup = BeautifulSoup(page.content, 'html.parser')
    return(soup)

# deprecado el 20200602
# def get_casos_recuperados(minsalsoup):
#     tables = minsalsoup.findAll('table')
#     for eachtable in tables:
#         rows = eachtable.findAll(lambda tag: tag.name == 'tr')
#         for row in rows:
#             cols = row.findAll('td')
#             cols = [ele.text.strip().replace('.', '') for ele in cols]
#             if cols[0] == 'Casos recuperados a nivel nacional':
#                 return cols


def get_casos_activos(minsalsoup):
    tables = minsalsoup.findAll('table')
    for eachtable in tables:
        rows = eachtable.findAll(lambda tag: tag.name == 'tr')
        for row in rows:
            cols = row.findAll('td')
            cols = [ele.text.strip().replace('.', '') for ele in cols]
            if cols[0] == 'Casos activos a nivel nacional':
                return cols

def get_fallecidos(minsalsoup):
    tables = minsalsoup.findAll('table')
    for eachtable in tables:
        rows = eachtable.findAll(lambda tag: tag.name == 'tr')
        for row in rows:
            cols = row.findAll('td')
            cols = [ele.text.strip().replace('.', '') for ele in cols]
            if cols[0] == 'Fallecidos a nivel nacional':
                return cols


def get_table_regional(minsalsoup):
    table = minsalsoup.find(lambda tag: tag.name == 'table')
    rows = table.findAll(lambda tag: tag.name == 'tr')
    data_minsal = []
    for row in rows:
        cols = row.findAll('td')
        cols = [ele.text.strip().replace('–', '0') for ele in cols]
        data_minsal.append([unidecode.unidecode(ele.replace('.', '').replace(',', '.').replace('\n', ' ')) for ele in cols if ele])
    data_clean = []
    for element in data_minsal:
        #normalize headers
        if len(element) == 4:
            element.insert(0, 'Region')
        # Sanity check: minsal table changes often
        if len(element) == 5:
            data_clean.append(element)

    print(data_clean)
    return data_clean


def writer(fileid, mylist, outputpath):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d")
    yesterday = now - timedelta(days=1)
    lastfiletimestamp = yesterday.strftime("%Y-%m-%d")
    lastfilename = outputpath + lastfiletimestamp + '-' + fileid + '.csv'
    #lastfilename='../output/producto4/2020-04-28-CasosConfirmados-totalRegional.csv'
    filename = outputpath + timestamp + '-' + fileid + '.csv'
    # Check if new data is the same as on last file in output

    print('Comparando valores de ' + filename + ' con ' + lastfilename)
    last_df = pd.read_csv(lastfilename)
    last_df_list = last_df.values.tolist()
    process = False
    if len(last_df_list) != len(mylist[1:]):
        print('yesterday\'s list was ' + str(len(last_df_list)) + ' elements long')
        #skip header as it changes often
        print('today\'s list is ' + str(len(mylist[1:])) + ' elements long')
        print('You should check minsal table to see what happened')
        #return
    else:
        i = 0
        while i < len(last_df_list):
            j = 0
            while j < len(last_df_list[i]):
                if str(last_df_list[i][j]).replace(' ', '') != str(mylist[i + 1][j]).replace(' ', ''):
                    print('de ayer : ' + str(last_df_list[i][j]).replace(' ', '') + ' no coincide con lo de hoy: ' + str(mylist[i + 1][j]).replace(' ', ''))
                    process = True
                j += 1
            i += 1

    if process:
        print('Escribiendo en ' + filename)
        with open(filename, 'w', newline='') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_NONE, escapechar=' ')
            for element in mylist:
                wr.writerow(element)
    else:
        raise Exception('La tabla de minsal no ha cambiado')


def prod5Nuevo(fte, producto):
    print('Generando nuevo producto5')
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d")
    myMinsalsoup = get_minsal_page(fte)
    tabla_regional = get_table_regional(myMinsalsoup)

    df_tr = pd.DataFrame.from_records(tabla_regional)

    header = (df_tr.loc[df_tr[0] == 'Region'])
    total = (df_tr.loc[df_tr[0] == 'Total'])
    a = header.append(total, ignore_index=True)
    print(a.to_string())
    #drop ** porcentaje casos fallecidos
    #print(a.columns)
    casos_activos = get_casos_activos(myMinsalsoup)
    fallecidos = get_fallecidos(myMinsalsoup)

    #'Region', 'Casos totales acumulados', 'Casos nuevos totales', 'Casos nuevos con sintomas', 'Casos nuevos sin sintomas*', 'Fallecidos', '% Total'
    a.rename(columns={0: 'Fecha', 1: 'Casos totales', 2: 'Casos nuevos totales',
                      3: 'Casos nuevos con sintomas', 4: 'Casos nuevos sin sintomas'}, inplace=True)
    a['Fecha'] = timestamp
    a.drop(0, inplace=True)

    a['Casos activos'] = casos_activos[1]
    a['Fallecidos'] = fallecidos[1]

    #print(a.to_string())
    totales = pd.read_csv(producto)
    #print(totales.columns[1:])
    # add Casos nuevos totales = Casos nuevos con sintomas + Casos nuevos sin sintomas
    for eachColumn in totales.columns[1:]:
        print('Checking if Casos nuevos totales is fine on ' + eachColumn)
        #print(totales.index[totales['Fecha'] == 'Casos nuevos con sintomas'].values[0])
        #print(totales.at[totales.index[totales['Fecha'] == 'Casos nuevos con sintomas'].values[0], eachColumn])
        rowConSintomas = totales.index[totales['Fecha'] == 'Casos nuevos con sintomas'].values[0]
        rowSinSintomas = totales.index[totales['Fecha'] == 'Casos nuevos sin sintomas'].values[0]
        rowCasosNuevosTotales = totales.index[totales['Fecha'] == 'Casos nuevos totales'].values[0]
        #print('row con ' + str(rowConSintomas))
        #print('row sin ' + str(rowSinSintomas))
        #print('expected is ' + str(totales.at[rowConSintomas, eachColumn]) + ' + ' + str(totales.at[rowSinSintomas, eachColumn]))
        #check for NaN
        if not np.isnan(totales.at[rowConSintomas, eachColumn]) and not np.isnan(totales.at[rowSinSintomas, eachColumn]):
            expectedTotal = totales.at[rowConSintomas, eachColumn] + totales.at[rowSinSintomas, eachColumn]
        elif not np.isnan(totales.at[rowConSintomas, eachColumn]) and np.isnan(totales.at[rowSinSintomas, eachColumn]):
            expectedTotal = totales.at[rowConSintomas, eachColumn]
        elif np.isnan(totales.at[rowConSintomas, eachColumn]) and not np.isnan(totales.at[rowSinSintomas, eachColumn]):
            expectedTotal = totales.at[rowSinSintomas, eachColumn]

        registeredTotal = totales.at[rowCasosNuevosTotales, eachColumn]
        if registeredTotal != expectedTotal:
            print('Casos nuevos totales debería ser ' + str(expectedTotal) + ' pero es ' + str(registeredTotal))
            #print(totales.at[rowCasosNuevosTotales, eachColumn])
            totales.at[rowCasosNuevosTotales, eachColumn] = expectedTotal
            #print(totales.at[rowCasosNuevosTotales, eachColumn])

    #print(totales.to_string())
    #normalizamos headers
    #expectedHeaders=['Casos nuevos con sintomas', 'Casos totales', 'Casos recuperados', 'Fallecidos',
     #               'Casos activos', 'Casos nuevos sin sintomas', 'Casos totales acumulados', 'Casos nuevos totales']
    emptyrow = [] * len(totales.columns)
    if 'Casos nuevos con sintomas' not in totales['Fecha'].values:
        totales['Fecha'][0] = 'Casos nuevos con sintomas'
    if 'Casos nuevos sin sintomas' not in totales['Fecha'].values:
        ax = ['Casos nuevos sin sintomas']
        bx = [''] * (len(totales.columns) - 1)
        ax.extend(bx)
        row = pd.DataFrame([ax], columns=totales.columns)
        aux = pd.concat([totales, row], ignore_index=True)
        totales = aux
        #totales['Fecha'][len(totales['Fecha']) + 1] = 'Casos nuevos sin sintomas'
    if 'Casos totales' not in totales['Fecha'].values:
        print('Casos totales not found')
        ax = ['Casos totales']
        bx = [''] * (len(totales.columns) - 1)
        ax.extend(bx)
        row = pd.DataFrame([ax], columns=totales.columns)
        aux = pd.concat([totales, row], ignore_index=True)
        totales = aux
    if 'Casos nuevos totales' not in totales['Fecha'].values:
        ax = ['Casos nuevos totales']
        bx = [''] * (len(totales.columns) - 1)
        ax.extend(bx)
        row = pd.DataFrame([ax], columns=totales.columns)
        aux = pd.concat([totales, row], ignore_index=True)
        totales = aux
        #print(totales)

    #print(totales['Fecha'])
    #print(a['Fecha'])
    if (a['Fecha'][1]) in totales.columns:
        print(a['Fecha'] + ' ya esta en el dataframe. No actualizamos')
        return
    else:
        #print(totales.iloc[:, 0])
        newColumn=[]
        #Need to add new rows to totales:
        for eachValue in totales.iloc[:, 0]:
            #print('each values is ' + eachValue)

            if eachValue in a.columns:
                #print(type(a[eachValue].values))
                newColumn.append(str(a[eachValue].values[0]))

            else:
                #print('appending ""')
                newColumn.append('')
        #print(newColumn)
        totales[timestamp] = newColumn
        totales.to_csv(producto, index=False)
        totales_t = totales.transpose()
        totales_t.to_csv(producto.replace('.csv', '_T.csv'), header=False)
        #print(totales.to_string())
        totales.rename(columns={'Fecha': 'Dato'}, inplace=True)
        identifiers = ['Dato']
        variables = [x for x in totales.columns if x not in identifiers]
        df_std = pd.melt(totales, id_vars=identifiers, value_vars=variables, var_name='Fecha',
                         value_name='Total')
        df_std.to_csv(producto.replace('.csv', '_std.csv'), index=False)


if __name__ == '__main__':

    #prod4('https://www.minsal.cl/nuevo-coronavirus-2019-ncov/casos-confirmados-en-chile-covid-19/', '../output/producto4/')

    prod5Nuevo('https://www.minsal.cl/nuevo-coronavirus-2019-ncov/casos-confirmados-en-chile-covid-19/', '../output/producto5/TotalesNacionales.csv')






