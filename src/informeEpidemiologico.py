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
Los productos que salen del informe epidemiologico son:
1
2
6
16
18
"""

import utils
import pandas as pd
from shutil import copyfile

def prod1(fte, producto):
    # Generando producto 1
    print('Generando producto 1')
    df = pd.read_csv(fte, dtype={'Codigo region': object, 'Codigo comuna': object})
    df.dropna(how='all', inplace=True)
    utils.regionName(df)
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
    utils.regionName(df)
    # Drop filas de totales por region
    todrop = df.loc[df['Comuna'] == 'Total']
    df.drop(todrop.index, inplace=True)
    print(df.columns)
    dates = []
    for eachColumn in df.columns:
        if '2020' in eachColumn:
            dates.append(eachColumn)
    print('las fechas son ' + str(dates))
    for eachdate in dates:
        filename = eachdate + '-CasosConfirmados.csv'
        print('escribiendo archivo ' + filename)
        aux = df[['Region', 'Codigo region', 'Comuna', 'Codigo comuna', 'Poblacion', eachdate]]
        aux.rename(columns={eachdate: 'Casos Confirmados'}, inplace=True)
        aux.to_csv(producto + filename, index=False)

def prod15(fte, producto):
    print('Generando producto 15')
    df = pd.read_csv(fte, dtype={'Codigo region': object, 'Codigo comuna': object})
    df.dropna(how='all', inplace=True)
    utils.regionName(df)
    # Drop filas de totales por region
    todrop = df.loc[df['Comuna'] == 'Total']
    df.drop(todrop.index, inplace=True)
    df.to_csv(producto + '.csv', index=False)
    df_t = df.T
    df_t.to_csv(producto + '_T.csv', header=False)
    copyfile('../input/SemanasEpidemiologicas.csv', '../output/producto15/SemanasEpidemiologicas.csv')

def prod16(fte, producto):
    print('Generando producto 16')
    copyfile(fte, producto + '.csv')
    df2_t = utils.transpone_csv(producto + '.csv')
    df2_t.to_csv(producto + '_T.csv', header=False)

if __name__ == '__main__':
    # Aqui se generan los productos 1 y 2 a partir del informe epidemiologico

    prod1('../input/CasosAcumuladosPorComuna.csv', '../output/producto1/Covid-19')

    prod2('../input/CasosAcumuladosPorComuna.csv', '../output/producto2/')

    print('Generando producto 6')
    exec(open('bulk_producto2.py').read())

    prod15('../input/FechaInicioSintomas.csv', '../output/producto15/Fecha_de_Inicio_de_Sintomas')

    prod16('../input/CasosGeneroEtario.csv', '../output/producto16/CasosGeneroEtario')