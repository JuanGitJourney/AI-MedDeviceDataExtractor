import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Function to add a title below the plot for APA 7 compliance
def add_title_below_plot(title, fig):
    fig.suptitle(title, y=-0.15, verticalalignment='bottom', fontsize=12)

# Load the CSV file
file_path = '../aiml_501ks.csv'
data = pd.read_csv(file_path)

# Converting 'date_received' and 'decision_date' to datetime format
data['date_received'] = pd.to_datetime(data['date_received'])
data['decision_date'] = pd.to_datetime(data['decision_date'])

# Calculating 'decision time' in days
data['decision_time'] = (data['decision_date'] - data['date_received']).dt.days

# Analyzing the 'device_classification_name' column
device_class_counts = data['device_classification_name'].value_counts()

# Splitting the 'device_classification_name' by commas and flattening the list
split_class_names = data['device_classification_name'].str.split(', ').explode()
split_class_name_counts = split_class_names.value_counts()

# Setting the font to Times New Roman for APA 7 compliance
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 12

# Increasing plot size and adjusting layout for clarity
plt.figure(figsize=(12, 8))
sns.histplot(data['decision_time'], bins=30, kde=True)
plt.xlabel('Decision Time (days)')
plt.ylabel('Frequency')
plt.tight_layout()
add_title_below_plot('Figure 1. Distribution of Decision Times', plt.gcf())
plt.show()

plt.figure(figsize=(12, 8))
sns.barplot(x=device_class_counts.head(10).values, y=device_class_counts.head(10).index)
plt.xlabel('Count')
plt.ylabel('Device Classification')
plt.tight_layout()
add_title_below_plot('Figure 2. Top 10 Device Classifications', plt.gcf())
plt.show()

plt.figure(figsize=(12, 8))
sns.barplot(x=split_class_name_counts.head(10).values, y=split_class_name_counts.head(10).index)
plt.xlabel('Count')
plt.ylabel('Terms')
plt.tight_layout()
add_title_below_plot('Figure 3. Top 10 Terms in Device Classifications After Splitting', plt.gcf())
plt.show()

# Grouping the data by 'date_received' and calculating the average 'decision_time'
time_series_data = data.groupby('date_received')['decision_time'].mean().reset_index()

# Plotting the time series data
plt.figure(figsize=(12, 8))
sns.lineplot(x='date_received', y='decision_time', data=time_series_data)
plt.xlabel('Date Received')
plt.ylabel('Average Decision Time (days)')
plt.title('Time Series of Average Decision Time')
plt.show()

# Calculating the number of devices per year
data['year'] = data['date_received'].dt.year
devices_per_year = data.groupby('year').size()

# Plotting the number of devices per year
plt.figure(figsize=(12, 8))
sns.barplot(x=devices_per_year.index, y=devices_per_year.values)
plt.xlabel('Year')
plt.ylabel('Number of Devices')
plt.title('Number of Devices per Year')
plt.xticks(rotation=45)
plt.show()