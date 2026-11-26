import csv


class readSheet:

    def __init__(self, filePath):
        self.filePath = filePath
        self.data = []
        self.dict_data = []

    def getData(self):

        # Clear old data every time the file is read
        self.data = []
        self.dict_data = []

        with open(
            self.filePath,
            newline="",
            encoding="utf-8-sig"
        ) as csvfile:

            # CSV files are comma-separated by default
            filereader = csv.reader(csvfile)

            for row in filereader:

                if row:
                    self.data.append(row)

        # Create dictionary version
        if self.data:

            headers = self.data[0]

            for row in self.data[1:]:

                self.dict_data.append(
                    dict(zip(headers, row))
                )

        return self.data




