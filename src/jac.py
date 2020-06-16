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

import pandas as pd

def prod40(fte, prod):
    df = pd.read_csv(fte, encoding='latin-1')

    #drop Region = Nan: includes all invalid dates
    df = df[df['Region_origen'].notna()]

    df['Cod_region_origen'] = df['Cod_region_origen'].astype(int)
    df['Cod_region_destino'] = df['Cod_region_destino'].astype(int)

    #stardardize fechas
    df['Inicio_semana'] = pd.to_datetime(df['Inicio_semana'], format='%d-%m-%Y')
    df['Fin_semana'] = pd.to_datetime(df['Fin_semana'], format='%d-%m-%Y')
    df['Inicio_semana'] = df['Inicio_semana'].astype(str)
    df['Fin_semana'] = df['Fin_semana'].astype(str)


    #drop columnas Año y mes
    df.drop(columns=['Año', 'Mes'], inplace=True)

    print(df.to_string())
    df.to_csv(prod + 'TransporteAereo_std.csv', index=False)


if __name__ == '__main__':
    print('Generating prod40')
    prod40('../input/JAC/TransporteAereo.csv', '../output/producto40/')
