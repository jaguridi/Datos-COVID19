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

"""
Los productos que salen de la contribucion de la UDD son:
34
"""

import pandas as pd
import glob
from utils import *
import numpy as np


def prod33(fte, prod):
    data = []
    for file in glob.glob(fte + '/*IM.csv'):
        print('Processing ' + file)
        df = pd.read_csv(file, sep=",", encoding="utf-8", decimal=",")

        # standardize column names
        df.rename(columns={'date': 'Fecha', 'comuna': 'Comuna'}, inplace=True)

        # hay 4 comunas perdidas 5502, 5703, 11302 12202
        # 5502, 5703 listas
        # 11302: O'Higgins no esta
        # 122012: Antartica no esta
        df = normalizaNombreCodigoRegionYComuna(df)
        df = FechaAlFinal(df)
        data.append(df)


    df = pd.concat(data)
    df = insertSuperficiePoblacion(df)
    df.dropna(how='any', inplace=True)

    #Ordenamos las columnas
    columns = ['Region', 'Codigo region', 'Comuna', 'Codigo comuna', 'Superficie_km2', 'Poblacion',
               'IM_interno', 'IM_externo', 'IM', 'Fecha']
    df = df[columns]
    df.to_csv(prod + '.csv', index=False)

    #try to build a single df with three rows per date per comuna
    aux = df.melt(id_vars=['Region', 'Codigo region', 'Comuna', 'Codigo comuna', 'Superficie_km2', 'Poblacion', 'Fecha'],
                  value_vars=['IM_interno', 'IM_externo', 'IM'])

    aux.to_csv(prod + '_std.csv', index=False)

    #IM_interno,IM_externo,IM,
    IMs = ['IM', 'IM_interno', 'IM_externo']
    for eachIM in IMs:
        columnsToDrop = [x for x in IMs if x != eachIM]
        df_aux = df.drop(columns=columnsToDrop)

        reshaped = pd.pivot_table(df_aux,
                            index=['Region', 'Codigo region', 'Comuna', 'Codigo comuna', 'Superficie_km2', 'Poblacion'],
                            columns=['Fecha'],
                            values=eachIM)

        reshaped.fillna(0, inplace=True)
        #reshaped = reshaped.applymap(np.int64)
        reshaped.to_csv(prod + '-' + eachIM + '.csv')
        data_t = reshaped.transpose()
        data_t.index.rename('', inplace=True)
        data_t.to_csv(prod + '-' + eachIM + '_T.csv')


if __name__ == '__main__':
    print('Generating producto 33')
    prod33('../input/UDD/', '../output/producto33/IndiceDeMovilidad')
