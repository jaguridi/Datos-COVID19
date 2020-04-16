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

import csv
import pandas as pd
from shutil import copyfile


def regionName(df):
    df["Region"] = df["Region"].replace({"Tarapaca": "Tarapacá", "Valparaiso": "Valparaíso",
                                         "Del Libertador General Bernardo O’Higgins": "O’Higgins", "Nuble": "Ñuble",
                                         "Biobio": "Biobío", "La Araucania": "Araucanía", "Los Rios": "Los Ríos",
                                         "Aysen": "Aysén", "Magallanes y la Antartica": "Magallanes"
                                         })
    return df


def prod1(fte, producto):
    # Generando producto 1
    print('Generando producto 1')
    df = pd.read_csv(fte, dtype={'Codigo region': object, 'Codigo comuna': object})
    df.dropna(how='all', inplace=True)
    regionName(df)
    # Drop filas de totales por region
    todrop = df.loc[df['Comuna'] == 'Total']
    df.drop(todrop.index, inplace=True)
    df.to_csv(producto + '.csv', index=False)
    df_t = df.T
    df_t.to_csv(producto + '_T.csv', header=False)

def prod2(fte, producto):
    print('Generando producto 2')
    df = pd.read_csv(fte, dtype={'Codigo region': object, 'Codigo comuna': object})
    df.dropna(how='all', inplace=True)
    regionName(df)
    # Drop filas de totales por region
    todrop = df.loc[df['Comuna'] == 'Total']
    df.drop(todrop.index, inplace=True)
    dates = []
    for eachColumn in df.columns:
        if '2020' in eachColumn:
            dates.append(eachColumn)
    print('las fechas son ' + str(dates))
    for eachdate in dates:
        filename = eachdate + '-CasosConfirmados.csv'
        print('escribiendo archivo ' + filename)
        aux = df[['Region', 'Codigo region', 'Comuna', 'Codigo comuna', 'Poblacion', eachdate]]
        aux.to_csv(producto + filename, index=False)


if __name__ == '__main__':
    # Aqui se generan los productos 1 y 2 a partir del informe epidemiologico

    #copyfile("../input/Covid-19.csv", "../output/producto1/Covid-19.csv")
    prod1('../input/CasosAcumuladosPorComuna.csv', '../output/producto1/Covid-19')

    prod2('../input/CasosAcumuladosPorComuna.csv', '../output/producto2/')

    # dates = []
    # with open('../input/Covid-19.csv') as csvfile:
    #     reader = csv.reader(csvfile, delimiter=',')
    #     header = ['Region', 'Codigo region', 'Comuna', 'Codigo comuna', 'Poblacion', 'Casos Confirmados']
    #     original_header = next(reader)
    #     dates = original_header[5:len(original_header)-1]
    #     print("las fechas son " + str(dates))
    #
    # for eachdate in dates:
    #     data = []
    #     data.append(header)
    #     with open('../input/Covid-19.csv') as csvfile:
    #         reader2 = csv.reader(csvfile, delimiter=',')
    #         next(reader2) # skip the header
    #
    #         output = "../output/producto2/" + eachdate + "-CasosConfirmados.csv"
    #         print("dumping " + eachdate + " to " + output)
    #         for row in reader2:
    #             #print(row)
    #             newrow = []
    #             for i in range(0, 5):
    #                 newrow.append(row[i])
    #             newrow.append(row[dates.index(eachdate)+5])
    #             data.append(newrow)
    #
    #     with open(output, "w") as f:
    #         writer = csv.writer(f)
    #         writer.writerows(data)
