# Header: This is the code responsible for reading a 
#csv file with a given set of data

import csv

class readSheet:
    filePath = ""
    data = []

    def __init__(filePath):
        self.filePath = filePath

    def getData() :  
        with open(filePath, newline='') as csvfile:
            filereader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in filereader:
                rowData = list
                rowData.append(row)
                data.append(rowData)


