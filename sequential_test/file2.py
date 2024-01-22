# def run():
# Import df.pkl

import pandas as pd
import numpy as np

df = pd.read_pickle('sequential_test/df.pkl')

# replace all string values in df to a random integer

df[df.select_dtypes(include=['object']).columns] = np.random.randint(0, 100, size=(len(df), len(df.select_dtypes(include=['object']).columns)))

# export df as pickle file

df.to_pickle('sequential_test/df.pkl')