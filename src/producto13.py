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


def producto13(producto5, producto10):
    print('generating producto13')
    df_recuperados = pd.read_csv(producto5)
    df_producto13 = df_recuperados
    df_fallecidos = pd.read_csv(producto10)
    df_fallecidos_total = pd.Series(df_fallecidos.sum())
    df_fallecidos_total = df_fallecidos_total[1:].transpose()
    df_producto13 = df_producto13.append(df_fallecidos_total, ignore_index=True)
    df_producto13.loc[1, 'Fecha'] = 'Fallecidos'
    return df_producto13


if __name__ == '__main__':

    df = producto13('../output/producto5/recuperados.csv', '../output/producto10/FallecidosEtario.csv')
    df.to_csv('../output/producto13/recuperados_fallecidos.csv', index=False)