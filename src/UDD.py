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
from datetime import datetime


def prod33(fte, prod):
    #data = []
    #for file in glob.glob(fte + '/*IM.csv'):
    #    print('Processing ' + file)

        # standardize column names

        # hay 4 comunas perdidas 5502, 5703, 11302 12202
        # 5502, 5703 listas
        # 11302: O'Higgins no esta
        # 122012: Antartica no esta
#        df = FechaAlFinal(df)
#        data.append(df)

#    df = pd.concat(data)

    # de aca parriba se va
    # 1.- leer un archivo
    # 1.5- estandarizar columnas
    df = pd.read_csv(fte, sep=";", encoding="utf-8", decimal=".")
    df.rename(columns={'date': 'Fecha', 'comuna': 'Comuna'}, inplace=True)
    df = pd.read_csv(fte, sep=";", encoding="utf-8", decimal=".")
    df.rename(columns={'date': 'Fecha', 'comuna': 'Comuna'}, inplace=True)

    df['Fecha'] = pd.to_datetime(df['Fecha'], format='%Y%m%d').dt.strftime("%Y-%m-%d")

    df = normalizaNombreCodigoRegionYComuna(df)
    df = insertSuperficiePoblacion(df)
    df.dropna(how='any', inplace=True)

    # 2.- comparar con output (duplicaciones/actualizaciones)

    df_old = pd.read_csv('../output/producto33/IndiceDeMovilidad-IM_old.csv', sep=",", encoding="utf-8", decimal=".")

    df.drop_duplicates(inplace=True)

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

   # columnas = list(data_t.columns.values)
   # columnas2 = list(df_old.columns.values)
   # print(columnas, columnas2)


if __name__ == '__main__':
    print('Generating producto 33')
    prod33('../input/UDD/indicadores_IM.csv', '../output/producto33/IndiceDeMovilidad')
