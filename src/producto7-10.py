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
from shutil import copyfile
import pandas as pd

# Estos productos salen del reporte diario del MINSAL

def transpone_csv(csvfile):
    df = pd.read_csv(csvfile)
    return(df.T)


if __name__ == '__main__':
    copyfile('../input/PCR.csv', '../output/producto7/PCR.csv')
    copyfile('../input/UCI.csv', '../output/producto8/UCI.csv')
    copyfile('../input/HospitalizadosUCIEtario.csv', '../output/producto9/HospitalizadosUCIEtario.csv')
    copyfile('../input/FallecidosEtario.csv', '../output/producto10/FallecidosEtario.csv')

    PCR_T = transpone_csv('../output/producto7/PCR.csv')
    PCR_T.to_csv('../output/producto7/PCR_T.csv', header=False)

    UCI_T = transpone_csv('../output/producto8/UCI.csv')
    UCI_T.to_csv('../output/producto8/UCI_T.csv', header=False)

    HospitalizadosUCIEtario_T = transpone_csv('../output/producto9/HospitalizadosUCIEtario.csv')
    HospitalizadosUCIEtario_T.to_csv('../output/producto9/HospitalizadosUCIEtario_T.csv', header=False)

    FallecidosEtario_T = transpone_csv('../output/producto10/FallecidosEtario.csv')
    FallecidosEtario_T.to_csv('../output/producto10/FallecidosEtario_T.csv', header=False)
