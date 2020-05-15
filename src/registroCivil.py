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



def prod31_32(fte,prod):
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

if __name__ == '__main__':
    print('Generando el producto 31')
    prod31_32('../input/RegistroCivil/', '../output/producto31/')

    print('Generando el producto 32')
    prod31_32('../input/RegistroCivil/', '../output/producto32/')
