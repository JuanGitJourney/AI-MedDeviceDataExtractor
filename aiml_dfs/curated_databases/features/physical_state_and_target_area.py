import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import textwrap

# Function to wrap text for long labels into multiple lines
def wrap_labels(labels, width=40):
    wrapped_labels = [textwrap.fill(label, width) for label in labels]
    return wrapped_labels

# Load the dataset
data = pd.read_excel('./final_device_features.xlsx', engine='openpyxl')


# Clean the data by removing rows where 'target_area' or 'physical_state' is NaN
cleaned_data = data.dropna(subset=['target_area', 'physical_state'])

# Count occurrences for 'target_area' and 'physical_state'
target_area_counts = cleaned_data['target_area'].value_counts()
physical_state_counts = cleaned_data['physical_state'].value_counts()

# Filter for values meeting the threshold
threshold = 5  # Adjust this threshold as needed
filtered_target_area_counts = target_area_counts[target_area_counts >= threshold]
filtered_physical_state_counts = physical_state_counts[physical_state_counts >= threshold]

# Calculate the percentage of included devices
total_devices = len(cleaned_data)
percentage_included_target_area = filtered_target_area_counts.sum() / total_devices * 100
percentage_included_physical_state = filtered_physical_state_counts.sum() / total_devices * 100

# Setting up the plot size and style
sns.set(style="whitegrid")

# Plot for 'target_area'
plt.figure(figsize=(12, 8))
sns.barplot(x=filtered_target_area_counts.values, y=filtered_target_area_counts.index)
plt.title('Occurrences of Target Area (Threshold = {}, {:.2f}% included)'.format(threshold, percentage_included_target_area))
plt.xlabel('Count')
plt.ylabel('Target Area')
plt.subplots_adjust(left=0.3)  # Adjust this value as needed to prevent cutting off text
plt.show()

# Pie chart for 'target_area'
plt.figure(figsize=(10, 10))
plt.pie(filtered_target_area_counts, labels=filtered_target_area_counts.index, autopct='%1.1f%%', startangle=140)
plt.title('Pie Chart of Target Area Occurrences')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.show()

# Wrapped labels for 'physical_state'
wrapped_physical_state_labels = wrap_labels(filtered_physical_state_counts.index)

# Plot for 'physical_state'
plt.figure(figsize=(12, 8))
ax = sns.barplot(x=filtered_physical_state_counts.values, y=wrapped_physical_state_labels)
plt.title('Occurrences of Physical State (Threshold = {}, {:.2f}% included)'.format(threshold, percentage_included_physical_state))
plt.xlabel('Count')
plt.ylabel('Physical State')
ax.set_yticklabels(wrapped_physical_state_labels)  # Set wrapped labels
plt.subplots_adjust(left=0.3)  # Adjust this value as needed to prevent cutting off text
plt.show()

# Pie chart for 'physical_state'
plt.figure(figsize=(10, 10))
plt.pie(filtered_physical_state_counts, labels=filtered_physical_state_counts.index, autopct='%1.1f%%', startangle=140)
plt.title('Pie Chart of Physical State Occurrences')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.show()