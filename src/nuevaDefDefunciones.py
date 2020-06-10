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
Los productos que salen del las nuevas definiciones son:
37
"""

from utils import *
import pandas as pd
import glob


# debe ser como el prod15 historico
# el nombre del archivo es el nombre de la serie
# formato definitivo:
# un solo archivo
# totales en primera fila
# cada fila es una fecha con las defunciones publicadas para ese dia por serie
# cada columna es una serie
def prod37(fte, producto):
    df_full = pd.read_excel(fte + 'Fallecidos Min Ciencias acumulado.xlsx')

    #convert 1st row as series name: Defunciones_fecha
    df_full.iloc[0, 1:] = df_full.iloc[0, 1:].astype(str)
    df_full.iloc[0, 1:] = df_full.iloc[0, 1:].replace(' 00:00:00', '', regex=True)
    #print(df_full.iloc[0, 1:])
    #print(df_full.to_string())
    df_full.iloc[0, 1:] = 'Defunciones_' + df_full.iloc[0, 1:]

    df_full.iloc[1:, 0] = df_full.iloc[1:, 0].astype(str)
    df_full.iloc[1:, 0] = df_full.iloc[1:, 0].replace(' 00:00:00', '', regex=True)
    #print(df_full.iloc[1:, 0])

    new_header = df_full.iloc[0]  # grab the first row for the header
    df_full = df_full[1:]  # take the data less the header row
    df_full.columns = new_header  # set the header row as the df header

    #producto T
    #print(df_full.to_string())
    df_full.to_csv(producto + '_T.csv', index=False)

    df_regular = df_full.T
    #print(df_regular.to_string())
    df_regular.rename(index={'Fecha': 'Publicacion'}, inplace=True)
    #print(df_regular.index)
    df_regular.to_csv(producto + '.csv', header=False)

    df_regular = pd.read_csv(producto + '.csv')
    #print(df_regular.to_string())

    identifiers = ['Publicacion']
    variables = [x for x in df_regular.columns if x not in identifiers]
    df_std = pd.melt(df_regular, id_vars=identifiers, value_vars=variables, var_name='Fecha',
                     value_name='Total')



    #print(df_std.to_string())
    df_std.to_csv(producto + '_std.csv', index=False)

    # data = []
    # for file in glob.glob(fte + '*.xlsx'):
    #     print(file)
    #     serie_name = file.replace(fte, '').replace('.xlsx', '')
    #     print(serie_name)
    #     df = pd.read_excel(file)
    #     df.columns = df.columns.str.lower()
    #     # need to drop total as fecha
    #     todrop = df.loc[df['fecha defunción'] == 'TOTAL']
    #     df.drop(todrop.index, inplace=True)
    #
    #     df['fecha defunción'] = df['fecha defunción'].dt.floor('d')
    #     df['Publicacion'] = serie_name
    #     print(df.columns)
    #     df = df.rename(columns={'fecha defunción': 'Fecha',
    #                             'n° fallecidos': 'Total',
    #                             'nº fallecidos': 'Total'
    #                             })
    #     columns_ordered = ['Publicacion', 'Fecha', 'Total']
    #     df = df[columns_ordered]
    #     df = df.dropna()
    #     #print(df)
    #     data.append(df)
    #
    # #este es el prod _std
    # data_std = pd.concat(data)
    # data_std.to_csv(producto + '_std.csv', index=False)
    #
    # # este es el prod _T
    # data_T = data_std.pivot(index='Fecha', columns='Publicacion', values='Total')
    # data_T.to_csv(producto + '_T.csv')
    #
    # # este es el prod  regular
    # data = data_T.T
    # data.to_csv(producto + '.csv')



if __name__ == '__main__':
    print('Generando producto 37')
    prod37('../input/NuevaDefDefunciones/', '../output/producto37/Defunciones')
