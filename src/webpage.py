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
4
5

"""
import requests
from bs4 import BeautifulSoup
import csv
import unidecode
import pandas as pd
from datetime import datetime, timedelta


def get_minsal_page(minsalURL):
    page = requests.get(minsalURL)
    soup = BeautifulSoup(page.content, 'html.parser')
    return(soup)

def get_casos_recuperados(minsalsoup):
    tables = minsalsoup.findAll('table')
    for eachtable in tables:
        rows = eachtable.findAll(lambda tag: tag.name == 'tr')
        for row in rows:
            cols = row.findAll('td')
            cols = [ele.text.strip().replace('.', '') for ele in cols]
            if cols[0] == 'Casos recuperados a nivel nacional':
                return cols


def get_table_regional(minsalsoup):
    table = minsalsoup.find(lambda tag: tag.name == 'table')
    rows = table.findAll(lambda tag: tag.name == 'tr')
    data_minsal = []
    for row in rows:
        cols = row.findAll('td')
        cols = [ele.text.strip().replace('–', '0') for ele in cols]
        data_minsal.append([unidecode.unidecode(ele.replace('.', '').replace(',', '.')) for ele in cols if ele])
    data_clean = []
    for element in data_minsal:
        # Sanity check: minsal table changes often
        if len(element) == 5:
            data_clean.append(element)
    return data_clean


def writer(fileid, mylist, outputpath):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d")
    yesterday = now - timedelta(days=1)
    lastfiletimestamp = yesterday.strftime("%Y-%m-%d")
    lastfilename = outputpath + lastfiletimestamp + '-' + fileid + '.csv'
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
        return
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

def add_row_to_csv(data, filename):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d")
    # if we already have the date we intend to insert, abort
    with open(filename) as csvfile:
        rows = csv.reader(csvfile, delimiter=',')
        for row in rows:
            if timestamp == row[0]:
                print('timestamp ' + timestamp + ' is already in ' + filename)
                return
    with open(filename, 'a') as myfile:
        print('Adding row to ' + filename)
        myfile.write("\n" + timestamp + ", " + data[1])
        myfile.close()


def add_column_to_csv(data, filename):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d")
    output = []
    # if we already have the date we intend to insert, abort
    with open(filename) as csvfile:
        rows = csv.reader(csvfile, delimiter=',')
        for index, row in enumerate(rows):
            if len(row) > 0 and (row[len(row)-1].strip()) == timestamp:
                print("comparing " + row[len(row) - 1].strip() + " with " + timestamp)
                print('timestamp ' + timestamp + ' is already in ' + filename)
                return
            else:
                if index == 0:
                    row.append(timestamp)
                if index == 1:
                    row.append(data[1])
            output.append(row)
    csvfile.close()

    with open(filename, 'w') as myfile:
        print('Dumping data to  ' + filename)
        myCsvwriter = csv.writer(myfile)
        for eachrow in output:
            myCsvwriter.writerow(eachrow)

def producto4(fte, producto):
    """
    Cada archivo en generado para producto4 corresponde a un csv que contiene los datos publicados por minsal en
    https://www.minsal.cl/nuevo-coronavirus-2019-ncov/casos-confirmados-en-chile-covid-19/
    """
    print('generando producto 4 a partir de ' + fte + ' en ' + producto)
    myMinsalsoup = get_minsal_page(fte)
    myTable = get_table_regional(myMinsalsoup)
    writer('CasosConfirmados-totalRegional', myTable, producto)


def producto5(fte, producto):
    """
    Producto5 correponde a un archivo csv que añande una columna con cada publicacion de casos recuperados en
    https://www.minsal.cl/nuevo-coronavirus-2019-ncov/casos-confirmados-en-chile-covid-19/
    """
    print('generando producto 5 a partir de ' + fte + ' en ' + producto)
    myMinsalsoup = get_minsal_page(fte)
    casos = get_casos_recuperados(myMinsalsoup)
    out = producto + 'recuperados.csv'
    # check if the file exist
    try:
        f = open(out)
    except FileNotFoundError:
        print(out + ' no existe, creando')
        with open(out, 'a+') as myfile:
            rows = ['Fecha\nRecuperados']
            for row in rows:
                myfile.write(row)
    add_column_to_csv(casos, out)


if __name__ == '__main__':
    # Aca se genera el producto 4 y 5
    test = False
    if test:
        producto4('https://www.minsal.cl/nuevo-coronavirus-2019-ncov/casos-confirmados-en-chile-covid-19/', '../temp/')
        producto5('https://www.minsal.cl/nuevo-coronavirus-2019-ncov/casos-confirmados-en-chile-covid-19/', '../temp/')

    else:
        producto4('https://www.minsal.cl/nuevo-coronavirus-2019-ncov/casos-confirmados-en-chile-covid-19/', '../output/producto4/')
        producto5('https://www.minsal.cl/nuevo-coronavirus-2019-ncov/casos-confirmados-en-chile-covid-19/', '../output/producto5/')