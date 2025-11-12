import pandas as pd
import numpy as np

bmw = pd.read_csv('BMW sales data (2010-2024) (1).csv')

#test to see if there are any null values
def check_null():
    print(bmw.isnull().sum())

print(bmw.Year.min())

print(bmw.Year.max())
