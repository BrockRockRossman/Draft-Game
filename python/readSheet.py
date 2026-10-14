# Header: This is the code responsible for reading a 
#csv file with a given set of data

import csv

class readSheet:
    filePath = ""
    data = []

    def __init__(self, filePath):
        self.filePath = filePath
        self.data = []

    def getData(self) :  
        with open(self.filePath, newline='') as csvfile:
            filereader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in filereader:
                rowData = list()
                rowData.append(row)
                self.data.append(rowData)


