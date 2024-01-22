# def run():
import pandas as pd
import numpy as np

# Create a random dataframe with 100 rows and 10 columns
data = np.random.choice(['string', 1, 2.5], size=(100, 10))

df = pd.DataFrame(data)
print(df)

# export df as pickle file
df.to_pickle('sequential_test/df.pkl')
