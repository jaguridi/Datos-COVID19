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
from shutil import copyfile


if __name__ == '__main__':
    # Aqui se generan los productos 1 y 2

    copyfile("../input/Covid-19.csv", "../output/producto1/Covid-19.csv")

    dates = []
    with open('../input/Covid-19.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        header = ['Region', 'Comuna', 'Poblacion', 'Casos Confirmados']
        original_header = next(reader)
        dates = original_header[3:len(original_header)-1]


    for eachdate in dates:
        data = []
        data.append(header)
        with open('../input/Covid-19.csv') as csvfile:
            reader2 = csv.reader(csvfile, delimiter=',')
            next(reader2) # skip the header

            output = "../output/producto2/" + eachdate + "-CasosConfirmados.csv"
            print("dumping " + eachdate + " to " + output)
            for row in reader2:
                newrow = []
                for i in range(0, 3):
                    newrow.append(row[i])
                newrow.append(row[dates.index(eachdate)+3])
                data.append(newrow)

        with open(output, "w") as f:
            writer = csv.writer(f)
            writer.writerows(data)
