# Header: This is the code responsible for reading a 
#csv file with a given set of data
import csv
# Imports
from csv import *

class readSheet:
    # Variables
    filePath = ""
    data = []
    dict_data = {}

    # Class initialization
    def __init__(self, filePath):
        self.filePath = filePath
        self.data = []

    # Method to get the data into the list
    def getData(self) :

        # Opens file
        with open(self.filePath, newline='', encoding='utf-8') as csvfile:

            #Creates a file reader
            filereader = csv.reader(csvfile, delimiter=' ', quotechar='|')

            # Reads the file row by row adding it to the list
            for row in filereader:

                rowData = list()
                rowData.append(row)
                self.data.append(rowData)

            # Creates a dictionary version of the same reader
            dictreader = csv.DictReader(csvfile, delimiter=' ', quotechar='|')

            # Reads the file row by row adding it to the list
            for row in dictreader:
                self.dict_data = row



