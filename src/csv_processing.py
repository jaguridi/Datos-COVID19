import csv



if __name__ == '__main__':

    dates = []
    with open('../input/Covid-19.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        header = ['Region', 'Comuna', 'Poblacion', 'Casos Confirmados']
        original_header = next(reader)
        dates = original_header[3:len(original_header)-1]
        # for row in reader:
        #     print(row)


    for eachdate in dates:
        data = []
        data.append(header)
        with open('../input/Covid-19.csv') as csvfile:
            reader2 = csv.reader(csvfile, delimiter=',')
            next(reader2) # skip the header

            output = "../output/CasosConfirmados-" + eachdate.replace('/', '-')
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





