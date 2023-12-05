import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re


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

# Group data by quarter and calculate the average decision time
grouped_data = data.groupby(data['date_received'].dt.to_period("M"))['decision_time'].mean()

# Grouping by year and counting the number of devices
trends_over_time = data.groupby(data['date_received'].dt.year).size()

# Categorization by Medical Specialty
medical_specialty_counts = data['regulation_medical_specialty'].value_counts()

# Convert the group by object to a DataFrame
grouped_data_df = grouped_data.reset_index()
grouped_data_df['date_received'] = grouped_data_df['date_received'].dt.to_timestamp()

# Analyzing the 'device_classification_name' column
device_class_counts = data['device_classification_name'].value_counts()

# Splitting the 'device_classification_name' by commas and flattening the list
split_class_names = data['device_classification_name'].str.split(', ').explode()
split_class_name_counts = split_class_names.value_counts()

# Setting the font to Times New Roman for APA 7 compliance
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 12

plt.figure(figsize=(12, 8))
sns.lineplot(x='date_received', y='decision_time', data=grouped_data_df)
plt.xlabel('Year')
plt.ylabel('Average Decision Time (days)')
plt.title('Trend of Decision Time Over Years')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('figure0_decision_time_trend.png')

plt.figure(figsize=(12, 8))
sns.histplot(data['decision_time'], bins=30, kde=True)
plt.xlabel('Decision Time (days)')
plt.ylabel('Frequency')
plt.tight_layout()
plt.savefig('figure1_decision_times.png')  # Saving the plot

plt.figure(figsize=(12, 8))
sns.barplot(x=device_class_counts.head(20).values, y=device_class_counts.head(20).index)
plt.xlabel('Count')
plt.ylabel('Device Classification')
plt.tight_layout()
plt.savefig('figure2_top_device_classifications.png')  # Saving the plot

plt.figure(figsize=(12, 8))
sns.barplot(x=split_class_name_counts.head(10).values, y=split_class_name_counts.head(10).index)
plt.xlabel('Count')
plt.ylabel('Terms')
plt.tight_layout()
plt.savefig('figure3_top_10_device_classifications_after_splitting.png')  # Saving the plot

# Grouping the data by 'date_received' and calculating the average 'decision_time'
time_series_data = data.groupby('date_received')['decision_time'].mean().reset_index()

# Plotting the time series data
plt.figure(figsize=(12, 8))
sns.lineplot(x='date_received', y='decision_time', data=time_series_data)
plt.xlabel('Date Received')
plt.ylabel('Average Decision Time (days)')
plt.title('Time Series of Average Decision Time')
plt.savefig('figure4_time_series_of_average_decision_time.png')  # Saving the plot

# Plotting the trends
plt.figure(figsize=(12, 8))
sns.lineplot(x=trends_over_time.index, y=trends_over_time.values)
plt.title('Trend of AI-Related Medical Device Clearances Over Time')
plt.xlabel('Year')
plt.ylabel('Number of Devices')
plt.savefig('figure5_ai_devices_cleareances_over_time.png')  # Saving the plot



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
# plt.show()

# Custom list of words to ignore
ignore_words = {'for', 'and', 'of', 'the', 'to', 'in', 'a', 'with', 'on', 'by', 'an', 'is', 'as', 'from', 'that'}


# Modified function to clean, split text into words, treat "x-ray" as a single word, and ignore specific words
def clean_and_split_modified(text):
    # Replace 'x-ray' with 'xray' to treat it as a single word
    text = text.lower().replace('x-ray', 'xray')

    # Remove special characters (except commas) and split into words
    words = re.findall(r'\b\w+\b', text)

    # Filter out ignored words
    words = [word for word in words if word not in ignore_words]
    return words


# Apply this function to each row in the 'device_classification_name' column and accumulate words
all_words_modified = []
for name in data['device_classification_name']:
    all_words_modified.extend(clean_and_split_modified(name))

# Count the frequency of each word
word_counts_modified = Counter(all_words_modified)

# Display the top 20 most common words
common_words_modified = dict(word_counts_modified.most_common(20))

# Create a bar plot
plt.figure(figsize=(12, 8))
plt.bar(common_words_modified.keys(), common_words_modified.values())
plt.xticks(rotation=45, ha="right")
plt.xlabel('Words')
plt.ylabel('Frequency')
plt.title('Top 20 Most Common Words in Device Classification Names (Adjusted)')
plt.tight_layout()



