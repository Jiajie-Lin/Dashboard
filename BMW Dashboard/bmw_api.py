"""
Jiajie Lin
BMW API
The primary API for interacting with the BMW dataset
"""

import pandas as pd
import numpy as np

import sankey as sk
import matplotlib.pyplot as plt

class BMWAPI():

    def load_data(self, filename):
        self.bmw = pd.read_csv(filename)


    def extract_local_network(self, att1, att2):

        bmw_df = self.bmw

        result = bmw_df.groupby([att1,att2]).size().reset_index(name = 'Count')

        return result

    #takes in a year and returns the the data of the column that matches that year
    def single(self,year,column):
        bmw_df = self.bmw

        filtered_year = bmw_df[bmw_df['Year'] == year]
        result = filtered_year.groupby([column]).size().reset_index(name = 'Count')


        return result[column]

    def get_attributes(self):
        """list of columns """
        return list(self.bmw.columns)

    def get_column_values(self,column):
        data = self.bmw
        return data[column]



def main():
    bmwapi = BMWAPI()
    bmwapi.load_data('BMW sales data (2010-2024) (1).csv')

    test = bmwapi.single(2021,'Engine_Size_L')
    print(test)
    pass
if __name__ == '__main__':
    main()


