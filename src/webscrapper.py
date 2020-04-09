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

import requests
from bs4 import BeautifulSoup
import csv
import unidecode
from datetime import datetime


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
                return(cols)


def get_table_regional(minsalsoup):
    table = minsalsoup.find(lambda tag: tag.name == 'table')
    #print(table.prettify())
    rows = table.findAll(lambda tag: tag.name == 'tr')
    data_minsal = []
    for row in rows:
        cols = row.findAll('td')
        cols = [ele.text.strip().replace('–', '0') for ele in cols]
        data_minsal.append([unidecode.unidecode(ele.replace('.', '')) for ele in cols if ele])
    data_clean = []
    for element in data_minsal:
        # Sanity check: minsal table changes often
        if len(element) == 5:
            data_clean.append(element)
    return data_clean


def writer(fileprefix, mylist):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d")
    filename = '../output/producto4/' + timestamp + '-' + fileprefix + '.csv'
    print('Writing to ' + filename)
    with open(filename, 'w', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_NONE, escapechar=' ')
        for element in mylist:
            wr.writerow(element)


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
            print("comparing " + row[len(row)-1].strip() + " with " + timestamp)
            if (row[len(row)-1].strip()) == timestamp:
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


if __name__ == '__main__':
    # Aca se genera el producto 4 y 5
    test = True
    myMinsalsoup = get_minsal_page(
        'https://www.minsal.cl/nuevo-coronavirus-2019-ncov/casos-confirmados-en-chile-covid-19/')
    if test:
        myMinsal = get_table_regional(myMinsalsoup)
        for element in myMinsal:
            print(element)
        casos = get_casos_recuperados(myMinsalsoup)
        print(casos)
        print('testing add_column_to_csv' )
        add_column_to_csv(casos, '../output/producto5/recuperados.csv' )

    else:

        writer('CasosConfirmados-totalRegional',
               get_table_regional(myMinsalsoup))
        casos = get_casos_recuperados(myMinsalsoup)
        add_row_to_csv(casos, '../output/producto5/recuperados.csv')