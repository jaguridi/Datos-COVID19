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
Los productos que salen del reporte diario son:
3
4
5
7
8
9
10
11
12
13
14
17
20
23
24
26
27
30
36
"""

import pandas as pd
from utils import *
from shutil import copyfile
from os import listdir
from os.path import isfile, join
from datetime import datetime, timedelta
import numpy as np


def prod4(fte, producto):
    print('Generando producto 4')
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    output = producto + today + '-CasosConfirmados-totalRegional.csv'
    df = pd.read_csv(fte, quotechar='"', sep=',', thousands=r'.', decimal=",")
    df.rename(columns={'Unnamed: 0': 'Region'}, inplace=True)
    if 'Unnamed: 7' in df.columns:
        df.drop(columns=['Unnamed: 7'], inplace=True)

    df_obj = df.select_dtypes(['object'])
    df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())
    regionName(df)
    df.at[16, 'Region'] = 'Total'
    # texttract reconoce 0 como o
    df.replace({'O': 0}, inplace=True)
    numeric_columns = [x for x in df.columns if x != 'Region']
    for i in numeric_columns:
        df[i] = df[i].astype(str)
        #df[i] = df[i].replace({r'\.': ''}, regex=True)
        df[i] = df[i].replace({r'\,': '.'}, regex=True)

    df.to_csv(output, index=False)

def prod5(fte, producto):
    print('Generando producto 5')
    # necesito series a nivel nacional por fecha:
    # Casos nuevos con sintomas
    # Casos totales
    # Casos recuperados  #ya no se reporta
    # Fallecidos
    # Casos activos
    # Casos nuevos sin sintomas

    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d")
    timestamp_dia_primero = now.strftime("%d-%m-%Y")
    df_input_file = pd.read_csv(fte + 'CasosConfirmadosTotales.csv')
    df_input_file['Fecha'] = pd.to_datetime(df_input_file['Fecha'], format='%d-%m-%Y')
    #print(df_input_file.to_string())
    #las columnas son :
    # Casos totales acumulados  Casos nuevos totales  Casos nuevos con sintomas  Casos nuevos sin sintomas*  Fallecidos totales % Total  Fecha

    df_input_file.rename(columns={'Casos totales acumulados': 'Casos totales',
                      'Casos nuevos totales': 'Casos nuevos totales',
                      'Casos nuevos con sintomas': 'Casos nuevos con sintomas',
                      'Casos nuevos sin sintomas*': 'Casos nuevos sin sintomas',
                      'Fallecidos totales': 'Fallecidos'}, inplace=True)

    #print(timestamp)
    timestamp = '2020-06-07'
    last_row = df_input_file[df_input_file['Fecha'] == timestamp]
    #print(last_row.to_string())

    df_output_file = pd.read_csv(producto)

    df_output_file = df_output_file.T
    df_output_file.columns = df_output_file.iloc[0]
    df_output_file.drop(df_output_file.index[0], inplace=True)

    df_output_file.index = pd.to_datetime(df_output_file.index, format='%Y-%m-%d')
    df_output_file.index.name = 'Fecha'
    #print(df_output_file.index)
    #print(last_row['Fecha'].values[0])
    if last_row['Fecha'].values[0] in df_output_file.index:
        print('Fecha was there, overwriting it')
        df_output_file.drop(last_row['Fecha'].values[0], axis=0, inplace=True)
        #print(df_output_file.to_string())
        last_row.index = last_row['Fecha']
        last_row.drop(columns=['Fecha'], inplace=True)
        df_output_file = df_output_file.append(last_row)
        #print(df_output_file.to_string())

    else:
        print('new date, adding row')
        last_row.index = last_row['Fecha']
        last_row.drop(columns=['Fecha'], inplace=True)
        df_output_file.append(last_row)

        ################################## Lo de Demian
        # Faltan  recuperados por FIS


    # despues hay que hacerlo solo para el ultimo valor
    # if df_input_file[(df_input_file['Fecha'] == date_before)]:
    #     print(df_input_file['Fecha'])
    #

    # el 2 de junio hubo un cambio: Casos activos y recuperados por FIS y FD se calculan a partir de ese dia.
    # antes de eso es None
    fecha_de_corte = datetime(2020, 6, 2)

    for i in df_output_file.index:
        if i >= fecha_de_corte:
            print(str(i))
            # Casos activos por FIS parten el 2 de Junio por definicion y corresponden a los casos activos del reporte diario
            df_output_file.loc[i, 'Casos activos por FIS'] = df_output_file.loc[i, 'Casos activos']
            # Recuperados FIS se calculan restando fallecidos y activos FIS
            df_output_file.loc[i, 'Casos recuperados por FIS'] = \
                df_output_file.loc[i, 'Casos totales'] - \
                df_output_file.loc[i, 'Casos activos'] - \
                df_output_file.loc[i, 'Fallecidos']
            # Falta casos activos y recuperados por FD: ocupar numeros antiguos para calcular
            fourteen_days = timedelta(days=14)

            # Casos activos por FD = casos activos hasta el 2 de Junio. Antes de eso se copian casos activos

            #df.loc[i, 'C'] = df.loc[i - 1, 'C'] * df.loc[i, 'A'] + df.loc[i, 'B']
            #print(i)
            if (i - fourteen_days) in df_output_file.index:
                #print('14 days ago is on the df')
                df_output_file.loc[i, 'Casos activos por FD'] = df_output_file.loc[i, 'Casos totales'] - df_output_file.loc[i - fourteen_days, 'Casos totales']
            else:
                print(str(i) + ' has no data 14 days ago')
                #df_output_file.loc[i, 'Casos activos por FD'] = df_output_file['Casos totales'] - \
                #                                    df_output_file.loc[i - fourteen_days_ago, 'Casos totales']

            # Es igual a recuperados hasta el 1 de junio (inclusive), desde el 2 se calcula
            # Recuperados FD se calculan restando fallecidos y activos FD
            df_output_file.loc[i, 'Casos recuperados por FD'] = (
                    df_output_file.loc[i, 'Casos totales'] -
                    df_output_file.loc[i, 'Casos activos por FD'] -
                    df_output_file.loc[i, 'Fallecidos'])

        # lo que pasa antes de la fecha de corte
        else:
            # Casos activos por FD = casos activos hasta el 2 de Junio. Antes de eso se copian casos activos
            df_output_file.loc[i, 'Casos activos por FD'] = df_output_file.loc[i, 'Casos activos']
            df_output_file.loc[i, 'Casos activos por FIS'] = np.NaN
            df_output_file.loc[i, 'Casos recuperados por FIS'] = np.NaN
            df_output_file.loc[i, 'Casos recuperados por FD'] = df_output_file.loc[i, 'Casos recuperados']

    ################################## Lo de Demian

    totales = df_output_file.T

    #print(totales.to_string())
    #print(totales.columns[1:])

    ## esto es estandar
    #totales = pd.read_csv(producto)
    #print(totales.columns.dtype)
    totales.columns = totales.columns.astype(str)

    totales.to_csv(producto, index_label='Fecha')
    totales_t = totales.transpose()
    totales_t.to_csv(producto.replace('.csv', '_T.csv'))
    print(totales.to_string())

    df_std = pd.melt(totales.reset_index(), id_vars='index', value_vars=totales.columns)
    df_std.rename(columns={'index': 'Dato', 'value': 'Total'}, inplace=True)
    #print(df_std.to_string())
    df_std.to_csv(producto.replace('.csv', '_std.csv'), index=False)


def prod3_13_14_26_27(fte):

    onlyfiles = [f for f in listdir(fte) if isfile(join(fte, f))]
    cumulativoCasosNuevos = pd.DataFrame({'Region': [],
                                          'Casos nuevos': []})
    cumulativoCasosTotales = pd.DataFrame({'Region': [],
                                           'Casos totales': []})
    cumulativoFallecidos = pd.DataFrame({'Region': [],
                                         'Fallecidos': []})
    casosNuevosConSintomas = pd.DataFrame({'Region': [],
                                         'Fecha': []})
    casosNuevosSinSintomas = pd.DataFrame({'Region': [],
                                         'Fecha': []})

    onlyfiles.sort()
    onlyfiles.remove('README.md')
    for eachfile in onlyfiles:
        print('processing ' + eachfile)
        date = eachfile.replace("-CasosConfirmados-totalRegional", "").replace(".csv", "")
        dataframe = pd.read_csv(fte + eachfile)
        # sanitize headers
        #print(eachfile)
        dataframe.rename(columns={'Región': 'Region'}, inplace=True)
        dataframe.rename(columns={'Casos  nuevos': 'Casos nuevos'}, inplace=True)
        dataframe.rename(columns={' Casos nuevos': 'Casos nuevos'}, inplace=True)
        dataframe.rename(columns={'Casos  nuevos  totales': 'Casos nuevos'}, inplace=True)
        dataframe.rename(columns={'Casos nuevos totales ': 'Casos nuevos'}, inplace=True)
        dataframe.rename(columns={'Casos nuevos totales': 'Casos nuevos'}, inplace=True)

        dataframe.rename(columns={'Casos  totales': 'Casos totales'}, inplace=True)
        dataframe.rename(columns={' Casos totales': 'Casos totales'}, inplace=True)
        dataframe.rename(columns={'Casos  totales  acumulados': 'Casos totales'}, inplace=True)
        dataframe.rename(columns={'Casos totales acumulados ': 'Casos totales'}, inplace=True)
        dataframe.rename(columns={'Casos totales acumulados': 'Casos totales'}, inplace=True)


        dataframe.rename(columns={' Casos fallecidos': 'Fallecidos'}, inplace=True)
        dataframe.rename(columns={'Fallecidos totales ': 'Fallecidos'}, inplace=True)
        dataframe.rename(columns={'Fallecidos totales': 'Fallecidos'}, inplace=True)

        dataframe.rename(columns={'Casos nuevos con síntomas': 'Casos nuevos con sintomas'}, inplace=True)
        dataframe.rename(columns={' Casos nuevos con síntomas': 'Casos nuevos con sintomas'}, inplace=True)
        dataframe.rename(columns={'Casos  nuevos  con  síntomas': 'Casos nuevos con sintomas'}, inplace=True)
        dataframe.rename(columns={'Casos nuevos con sintomas': 'Casos nuevos con sintomas'}, inplace=True)
        dataframe.rename(columns={' Casos nuevos con sintomas': 'Casos nuevos con sintomas'}, inplace=True)
        dataframe.rename(columns={'Casos  nuevos  con  sintomas': 'Casos nuevos con sintomas'}, inplace=True)
        dataframe.rename(columns={'Casos nuevos con sintomas ': 'Casos nuevos con sintomas'}, inplace=True)

        dataframe.rename(columns={'Casos nuevos sin síntomas': 'Casos nuevos sin sintomas'}, inplace=True)
        dataframe.rename(columns={' Casos nuevos sin síntomas': 'Casos nuevos sin sintomas'}, inplace=True)
        dataframe.rename(columns={'Casos  nuevos  sin  síntomas': 'Casos nuevos sin sintomas'}, inplace=True)
        dataframe.rename(columns={'Casos nuevos sin síntomas*': 'Casos nuevos sin sintomas'}, inplace=True)
        dataframe.rename(columns={' Casos nuevos sin síntomas*': 'Casos nuevos sin sintomas'}, inplace=True)
        dataframe.rename(columns={'Casos  nuevos  sin  síntomas*': 'Casos nuevos sin sintomas'}, inplace=True)
        dataframe.rename(columns={'Casos nuevos sin sintomas': 'Casos nuevos sin sintomas'}, inplace=True)
        dataframe.rename(columns={' Casos nuevos sin sintomas': 'Casos nuevos sin sintomas'}, inplace=True)
        dataframe.rename(columns={'Casos  nuevos  sin  sintomas': 'Casos nuevos sin sintomas'}, inplace=True)
        dataframe.rename(columns={'Casos nuevos sin sintomas*': 'Casos nuevos sin sintomas'}, inplace=True)
        dataframe.rename(columns={' Casos nuevos sin sintomas*': 'Casos nuevos sin sintomas'}, inplace=True)
        dataframe.rename(columns={'Casos  nuevos  sin  sintomas*': 'Casos nuevos sin sintomas'}, inplace=True)
        dataframe.rename(columns={'Casos nuevos sin sintomas* ': 'Casos nuevos sin sintomas'}, inplace=True)

        if cumulativoCasosNuevos['Region'].empty:
            cumulativoCasosNuevos[['Region', 'Casos nuevos']] = dataframe[['Region', 'Casos nuevos']]
            cumulativoCasosNuevos.rename(columns={'Casos nuevos': date}, inplace=True)
            cumulativoCasosTotales[['Region', 'Casos totales']] = dataframe[['Region', 'Casos totales']]
            cumulativoCasosTotales.rename(columns={'Casos totales': date}, inplace=True)
        else:
            print(dataframe.columns)
            cumulativoCasosNuevos[date] = dataframe['Casos nuevos']
            cumulativoCasosTotales[date] = dataframe['Casos totales']

        if 'Fallecidos' in dataframe.columns:
            if cumulativoFallecidos['Region'].empty:
                cumulativoFallecidos[['Region', 'Fallecidos']] = dataframe[['Region', 'Fallecidos']]
                cumulativoFallecidos.rename(columns={'Fallecidos': date}, inplace=True)
            else:
                cumulativoFallecidos[date] = dataframe['Fallecidos']

        if 'Casos nuevos con sintomas' in dataframe.columns:
            if casosNuevosConSintomas['Region'].empty:
                casosNuevosConSintomas[['Region', 'Fecha']] = dataframe[['Region', 'Casos nuevos con sintomas']]
                casosNuevosConSintomas.rename(columns={'Fecha': date}, inplace=True)
            else:
                casosNuevosConSintomas[date] = dataframe['Casos nuevos con sintomas']
        else:
            date2 = (pd.to_datetime(date)).strftime('%Y-%m-%d')
            if date2 < '2020-04-29':
                if casosNuevosConSintomas['Region'].empty:
                    casosNuevosConSintomas[['Region', 'Fecha']] = dataframe[['Region','Casos nuevos']]
                    casosNuevosConSintomas.rename(columns={'Fecha': date}, inplace=True)
                else:
                    casosNuevosConSintomas[date] = dataframe['Casos nuevos']


        if 'Casos nuevos sin sintomas' in dataframe.columns:
            if casosNuevosSinSintomas['Region'].empty:
                casosNuevosSinSintomas[['Region', 'Fecha']] = dataframe[['Region', 'Casos nuevos sin sintomas']]
                casosNuevosSinSintomas.rename(columns={'Fecha': date}, inplace=True)
            else:
                casosNuevosSinSintomas[date] = dataframe['Casos nuevos sin sintomas']



    # estandarizar nombres de regiones
    regionName(cumulativoCasosNuevos)
    regionName(cumulativoCasosTotales)
    regionName(cumulativoFallecidos)
    regionName(casosNuevosConSintomas)
    regionName(casosNuevosSinSintomas)

    cumulativoCasosNuevos_T = cumulativoCasosNuevos.transpose()
    cumulativoCasosTotales_T = cumulativoCasosTotales.transpose()
    cumulativoFallecidos_T = cumulativoFallecidos.transpose()
    casosNuevosConSintomas_T = casosNuevosConSintomas.transpose()
    casosNuevosSinSintomas_T = casosNuevosSinSintomas.transpose()

    #### PRODUCTO 3
    cumulativoCasosTotales.to_csv('../output/producto3/CasosTotalesCumulativo.csv', index=False)
    cumulativoCasosTotales_T.to_csv('../output/producto3/CasosTotalesCumulativo_T.csv', header=False)
    identifiers = ['Region']
    variables = [x for x in cumulativoCasosTotales.columns if x not in identifiers]
    df_std = pd.melt(cumulativoCasosTotales, id_vars=identifiers, value_vars=variables, var_name='Fecha',
                     value_name='Total')
    df_std.to_csv('../output/producto3/CasosTotalesCumulativo_std.csv', index=False)

    #### PRODUCTO 13
    cumulativoCasosNuevos.to_csv('../output/producto13/CasosNuevosCumulativo.csv', index=False)
    cumulativoCasosNuevos_T.to_csv('../output/producto13/CasosNuevosCumulativo_T.csv', header=False)
    identifiers = ['Region']
    variables = [x for x in cumulativoCasosTotales.columns if x not in identifiers]
    df_std = pd.melt(cumulativoCasosNuevos, id_vars=identifiers, value_vars=variables, var_name='Fecha',
                     value_name='Total')
    df_std.to_csv('../output/producto13/CasosNuevosCumulativo_std.csv', index=False)

    #### PRODUCTO 14
    cumulativoFallecidos.to_csv('../output/producto14/FallecidosCumulativo.csv', index=False)
    cumulativoFallecidos_T.to_csv('../output/producto14/FallecidosCumulativo_T.csv', header=False)
    identifiers = ['Region']
    variables = [x for x in cumulativoFallecidos.columns if x not in identifiers]
    df_std = pd.melt(cumulativoFallecidos, id_vars=identifiers, value_vars=variables, var_name='Fecha',
                     value_name='Total')
    df_std.to_csv('../output/producto14/FallecidosCumulativo_std.csv', index=False)

    #### PRODUCTO 26
    casosNuevosConSintomas.to_csv('../output/producto26/CasosNuevosConSintomas.csv', index=False)
    casosNuevosConSintomas_T.to_csv('../output/producto26/CasosNuevosConSintomas_T.csv', header=False)
    identifiers = ['Region']
    variables = [x for x in casosNuevosConSintomas.columns if x not in identifiers]
    df_std = pd.melt(casosNuevosConSintomas, id_vars=identifiers, value_vars=variables, var_name='Fecha',
                     value_name='Casos confirmados')
    df_std.to_csv('../output/producto26/CasosNuevosConSintomas_std.csv', index=False)

    #### PRODUCTO 27
    casosNuevosSinSintomas.to_csv('../output/producto27/CasosNuevosSinSintomas.csv', index=False)
    casosNuevosSinSintomas_T.to_csv('../output/producto27/CasosNuevosSinSintomas_T.csv', header=False)
    identifiers = ['Region']
    variables = [x for x in casosNuevosSinSintomas.columns if x not in identifiers]
    df_std = pd.melt(casosNuevosSinSintomas, id_vars=identifiers, value_vars=variables, var_name='Fecha',
                     value_name='Casos confirmados')
    df_std.to_csv('../output/producto27/CasosNuevosSinSintomas_std.csv', index=False)


def prod7_8(fte, producto):
    df = pd.read_csv(fte, dtype={'Codigo region': object})
    regionName(df)
    df = df.replace('-', '', regex=True)
    df_t = df.T
    df.to_csv(producto + '.csv', index=False)
    df_t.to_csv(producto + '_T.csv', header=False)
    identifiers = ['Region', 'Codigo region', 'Poblacion']
    variables = [x for x in df.columns if x not in identifiers]
    df_std = pd.melt(df, id_vars=identifiers, value_vars=variables, var_name='fecha', value_name='numero')
    df_std.to_csv(producto + '_std.csv', index=False)


def prod9_10(fte, producto):
    copyfile(fte, producto + '.csv')
    HospitalizadosUCIEtario_T = transpone_csv(producto + '.csv')
    HospitalizadosUCIEtario_T.to_csv(producto + '_T.csv', header=False)
    df = pd.read_csv(fte)
    identifiers = ['Grupo de edad']
    variables = [x for x in df.columns if x not in identifiers]
    df_std = pd.melt(df, id_vars=identifiers, value_vars=variables, var_name='fecha', value_name='Casos confirmados')
    df_std.to_csv(producto + '_std.csv', index=False)


def prod17(fte, producto):
    copyfile(fte, producto + '.csv')
    df = pd.read_csv(fte)
    df_t = df.T
    df_t.to_csv(producto + '_T.csv', header=False)
    identifiers = ['Establecimiento', 'Examenes']
    variables = [x for x in df.columns if x not in identifiers]
    df_std = pd.melt(df, id_vars=identifiers, value_vars=variables, var_name='fecha', value_name='Numero de PCR')
    df_std.to_csv(producto + '_std.csv', index=False)


def prod20(fte, producto):
    copyfile(fte, producto + '.csv')
    df = pd.read_csv(fte)
    df_t = df.T
    df_t.to_csv(producto + '_T.csv', header=False)
    identifiers = ['Ventiladores']
    variables = [x for x in df.columns if x not in identifiers]
    df_std = pd.melt(df, id_vars=identifiers, value_vars=variables, var_name='fecha', value_name='numero')
    df_std.to_csv(producto + '_std.csv', index=False)


def prod23(fte, producto):
    copyfile(fte, producto + '.csv')
    df = pd.read_csv(fte)
    df_t = df.T
    df_t.to_csv(producto + '_T.csv', header=False)
    identifiers = ['Casos']
    variables = [x for x in df.columns if x not in identifiers]
    df_std = pd.melt(df, id_vars=identifiers, value_vars=variables, var_name='fecha', value_name='Casos confirmados')
    df_std.to_csv(producto + '_std.csv', index=False)


def prod24(fte, producto):
    copyfile(fte, producto + '.csv')
    df = pd.read_csv(fte)
    df_t = df.T
    df_t.to_csv(producto + '_T.csv', header=False)
    identifiers = ['Tipo de cama']
    variables = [x for x in df.columns if x not in identifiers]
    df_std = pd.melt(df, id_vars=identifiers, value_vars=variables, var_name='fecha', value_name='Casos confirmados')
    df_std.to_csv(producto + '_std.csv', index=False)


def prod30(fte, producto):
    copyfile(fte, producto + '.csv')
    df = pd.read_csv(fte)
    df_t = df.T
    df_t.to_csv(producto + '_T.csv', header=False)
    identifiers = ['Casos']
    variables = [x for x in df.columns if x not in identifiers]
    df_std = pd.melt(df, id_vars=identifiers, value_vars=variables, var_name='Fecha', value_name='Casos confirmados')
    df_std.to_csv(producto + '_std.csv', index=False)


def prod36(fte, producto):
    copyfile(fte, producto + '.csv')
    df = pd.read_csv(fte)
    df_t = df.T
    df_t.to_csv(producto + '_T.csv', header=False)
    identifiers = ['Region','Categoria']
    variables = [x for x in df.columns if x not in identifiers]
    df_std = pd.melt(df, id_vars=identifiers, value_vars=variables, var_name='Fecha',
                     value_name='Numero')
    df_std.to_csv(producto + '_std.csv', index=False)


if __name__ == '__main__':

    # prod4('../input/ReporteDiario/CasosConfirmados.csv', '../output/producto4/')
    #
    prod5('../input/ReporteDiario/', '../output/producto5/TotalesNacionales.csv')
    #
    # print('Generando productos 3, 13, 14, 26 y 27')
    # prod3_13_14_26_27('../output/producto4/')
    #
    # print('Generando producto 11')
    # print('Generando producto 11: bulk_producto4.py hay un bug, debes generarlo a mano')
    # # exec(open('bulk_producto4.py').read())
    #
    # print('Generando producto 7')
    # prod7_8('../input/ReporteDiario/PCR.csv', '../output/producto7/PCR')
    #
    # print('Generando producto 8')
    # prod7_8('../input/ReporteDiario/UCI.csv', '../output/producto8/UCI')
    #
    # print('Generando producto 9')
    # prod9_10('../input/ReporteDiario/HospitalizadosUCIEtario.csv', '../output/producto9/HospitalizadosUCIEtario')
    #
    # print('Generando producto 10')
    # prod9_10('../input/ReporteDiario/FallecidosEtario.csv', '../output/producto10/FallecidosEtario')
    #
    # print('Generando producto 12')
    # exec(open('bulk_producto7.py').read())
    #
    # print('Generando producto 17')
    # # copyfile('../input/ReporteDiario/PCREstablecimiento.csv', '../output/producto17/PCREstablecimiento.csv')
    # prod17('../input/ReporteDiario/PCREstablecimiento.csv', '../output/producto17/PCREstablecimiento')
    #
    # print('Generando producto 20')
    # prod20('../input/ReporteDiario/NumeroVentiladores.csv', '../output/producto20/NumeroVentiladores')
    #
    # print('Generando producto 23')
    # prod23('../input/ReporteDiario/PacientesCriticos.csv', '../output/producto23/PacientesCriticos')
    #
    # print('Generando producto 24')
    # prod24('../input/ReporteDiario/CamasHospital_Diario.csv', '../output/producto24/CamasHospital_Diario')
    #
    # print('Generando producto 30')
    # prod30('../input/ReporteDiario/PacientesVMI.csv', '../output/producto30/PacientesVMI')
    #
    # print('Generando producto 36')
    # prod36('../input/ReporteDiario/ResidenciasSanitarias.csv', '../output/producto36/ResidenciasSanitarias')
