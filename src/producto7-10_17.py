"""
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
"""

from shutil import copyfile
import pandas as pd

# Estos productos salen del reporte diario del MINSAL


def transpone_csv(csvfile):
    df = pd.read_csv(csvfile)
    return(df.T)


def regionName(df):
    df["Region"] = df["Region"].replace({"Tarapaca": "Tarapacá", "Valparaiso": "Valparaíso",
                                         "Del Libertador General Bernardo O’Higgins": "O’Higgins", "Nuble": "Ñuble",
                                         "Biobio": "Biobío", "La Araucania": "Araucanía", "Los Rios": "Los Ríos",
                                         "Aysen": "Aysén", "Magallanes y la Antartica": "Magallanes"
                                         })
    return df


def prod7_8(fte, producto):
    print('Generando producto ' + producto)
    df = pd.read_csv(fte, dtype={'Codigo region': object})
    regionName(df)
    df_t = df.T
    df.to_csv(producto + '.csv', index=False)
    df_t.to_csv(producto + '_T.csv', header=False)


if __name__ == '__main__':

    prod7_8('../input/PCR.csv', '../output/producto7/PCR')

    prod7_8('../input/UCI.csv', '../output/producto8/UCI')

    copyfile('../input/HospitalizadosUCIEtario.csv', '../output/producto9/HospitalizadosUCIEtario.csv')
    HospitalizadosUCIEtario_T = transpone_csv('../output/producto9/HospitalizadosUCIEtario.csv')
    HospitalizadosUCIEtario_T.to_csv('../output/producto9/HospitalizadosUCIEtario_T.csv', header=False)

    copyfile('../input/FallecidosEtario.csv', '../output/producto10/FallecidosEtario.csv')
    FallecidosEtario_T = transpone_csv('../output/producto10/FallecidosEtario.csv')
    FallecidosEtario_T.to_csv('../output/producto10/FallecidosEtario_T.csv', header=False)

    copyfile('../input/PCREstablecimiento.csv', '../output/producto17/PCREstablecimiento.csv')
