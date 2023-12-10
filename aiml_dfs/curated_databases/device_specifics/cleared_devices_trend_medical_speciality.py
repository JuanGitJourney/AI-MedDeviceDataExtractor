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

# Grouping the data by 'decision_year' and 'regulation_medical_specialty' and counting the number of devices
cleared_devices_per_year = data.groupby(['decision_year', 'regulation_medical_specialty']).size().reset_index(name='count')

# Sorting the results for better readability
cleared_devices_per_year_sorted = cleared_devices_per_year.sort_values(by=['decision_year', 'regulation_medical_specialty'])

print(cleared_devices_per_year_sorted.head(10))  # Displaying the first 10 rows of the sorted result

plt.figure(figsize=(15, 10))

# Create a bar plot
sns.barplot(x='decision_year', y='count', hue='regulation_medical_specialty', data=cleared_devices_per_year_sorted)

# Adding titles and labels
plt.title('Number of Cleared Devices Per Year by Medical Specialty')
plt.xlabel('Year')
plt.ylabel('Number of Cleared Devices')
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.legend(title='Medical Specialty', bbox_to_anchor=(1.05, 1), loc='upper left')  # Adjust legend position

# Show the plot
plt.tight_layout()  # Adjust layout to fit everything
plt.show()
