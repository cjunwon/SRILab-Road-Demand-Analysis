# def run():
import pandas as pd
import numpy as np

# import df.pkl

df = pd.read_pickle('sequential_test/df.pkl')

# print number of string values in df

print(len(df[df.select_dtypes(include=['object']).columns]))