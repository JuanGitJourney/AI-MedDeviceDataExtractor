import pandas as pd

# Load data
file_path = '../final_database.xlsx'
data = pd.read_excel(file_path, engine='openpyxl')

# Descriptive statistics for all columns, including categorical
print("\nDescriptive Statistics for All Data:")
print(data.describe(include='all'))

# Computing specific statistics
print("\nMean Values:")
print(data.mean())

print("\nMedian:")
print(data.median())

print("\nMode:")
print(data.mode())

print("\nStandard deviation:")
print(data.std())

print("\nVariance:")
print(data.var())


