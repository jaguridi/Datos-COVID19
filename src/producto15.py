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
from shutil import copyfile

# el producto 15 y 16 dependen del informe epidemiologico

def transpone_csv(csvfile):
    df = pd.read_csv(csvfile)
    return(df.T)


if __name__ == '__main__':

    copyfile('../input/Fecha_de_inicio_de_Sintomas.csv', '../output/producto15/Fecha_de_inicio_de_Sintomas.csv')
    copyfile('../input/SemanasEpidemiologicas.csv', '../output/producto15/SemanasEpidemiologicas.csv')

    df_t = transpone_csv('../output/producto15/Fecha_de_inicio_de_Sintomas.csv')
    df_t.to_csv('../output/producto15/Fecha_de_inicio_de_Sintomas_T.csv', header=False)