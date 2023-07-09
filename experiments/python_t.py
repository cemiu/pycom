import pandas as pd

# sample df with column A, nums from 0 to 100
df = pd.DataFrame({'A': range(100)})
print(df)

example_function = lambda x: x ** 2

# create new column B, apply example_function to column A
df['B'] = df['A'].apply(example_function)
print(df)
