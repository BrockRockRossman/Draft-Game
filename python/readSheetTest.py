
import unittest
from readSheet import readSheet

class readSheetTest(unittest.TestCase):

    # Test filePath
    # /Users/brockrossman/onedrive/04_college/26-27/Softwater/Draft-Game/files/TestSheet1.csv
    filePath = '/Users/brockrossman/onedrive/04_college/26-27/Softwater/Draft-Game/files/baseTest.csv'

    expected_data = [
        ['row 1', 'A', 'a'], 
        ['row 2', 'B', 'b'], 
        ['row 3', 'C', 'c']
        ] # Expected data from the test CSV file

    newSheet = None

    def setUp(self):
        self.newSheet = readSheet('/Users/brockrossman/onedrive/04_college/26-27/Softwater/Draft-Game/files/baseTest.csv')

    def test_Filepath(self):
        self.setUp()
        self.assertEqual(self.newSheet.filePath, self.filePath) # Checks that filepath was set correctly
        

    def test_GetData(self):
        self.setUp()
        self.newSheet.getData()
        self.assertEqual(self.newSheet.data, self.expected_data) # Checks that data was read correctly
    

unittest.main()