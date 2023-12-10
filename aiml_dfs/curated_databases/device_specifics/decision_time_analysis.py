import pandas as pd
import scipy.stats as stats
from scipy.stats import kruskal, mannwhitneyu
import statsmodels.api as sm
from statsmodels.formula.api import ols
import statsmodels.formula.api as smf 
import matplotlib.pyplot as plt
import seaborn as sns



# Load the data
file_path = '../final_database.xlsx'  
data = pd.read_excel(file_path, engine='openpyxl')

# Combine the three columns into a single datetime column
data['date_received'] = pd.to_datetime({'year': data['year_received'], 'month': data['month_received'], 'day': data['day_received']})
data['decision_date'] = pd.to_datetime({'year': data['decision_year'], 'month': data['decision_month'], 'day': data['decision_day']})

# Calculating 'decision time' in days
data['decision_time'] = (data['decision_date'] - data['date_received']).dt.days


print("\nMean Values:")
print(data['decision_time'].mean())

print("\nMedian:")
print(data['decision_time'].median())

print("\nMode:")
print(data['decision_time'].mode())

print("\nStandard deviation:")
print(data['decision_time'].std())

print("\nVariance:")
print(data['decision_time'].var())




# Dropping NaN values for the analysis
#data.dropna(subset=['device_classification_name', 'review_panel', 'decision_time'], inplace=True)
data = data.dropna(subset=['decision_time', 'device_classification_name', 'review_panel'])

# Non-Parametric Tests
# Kruskal-Wallis Test - comparing 'decision_time' across different 'device_classification_name'
kruskal_test = kruskal(*[group["decision_time"].values for name, group in data.groupby("device_classification_name")])
print("Kruskal-Wallis Test (Device Classification):", kruskal_test)

# Mann-Whitney U Test - comparing 'decision_time' between two groups from 'review_panel'
# Note: Choose two specific groups for comparison
group1 = data['decision_time'][data['review_panel'] == 'Group1'].values
group2 = data['decision_time'][data['review_panel'] == 'Group2'].values
mannwhitney_test = mannwhitneyu(group1, group2)
print("Mann-Whitney U Test (Review Panel Group1 vs Group2):", mannwhitney_test)







# Dropping NaN values for the analysis
data2 = data.dropna(subset=['decision_time', 'review_panel'])

# Explore the unique values in 'review_panel' to understand how to stratify the data
unique_review_panels = data2['review_panel'].unique()
print("Unique Review Panels:", unique_review_panels)

for panel in data2['review_panel'].unique():
    print(panel, ":\n", data2[data2['review_panel'] == panel]['decision_time'].describe(), "\n")

# Boxplot for visual comparison
plt.figure(figsize=(200, 8))
sns.boxplot(x='review_panel', y='decision_time', data=data2)
plt.xticks(rotation=30)
plt.title('Decision Times Across Review Panels')
plt.xlabel('Review Panel')
plt.ylabel('Decision Time (days)')
plt.show()

# Kruskal-Wallis test
kruskal_results = kruskal(*[group["decision_time"].values for name, group in data2.groupby("review_panel")])
print("Kruskal-Wallis Test Across Review Panels:", kruskal_results)





