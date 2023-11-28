import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the updated data
df = pd.read_csv('./devices_features.csv', delimiter=',')

# Prepare data for plots
device_class_counts = df['device_class'].value_counts()
medical_specialty_counts = df['medical_specialty'].value_counts()
third_party_review_counts = df['third_party_review'].value_counts()
gmp_exempt_counts = df['gmp_exempt_flag'].value_counts()
implant_counts = df['implant_flag'].value_counts()
life_sustain_counts = df['life_sustain_flag'].value_counts()

# Setting up the figure for multiple plots
plt.figure(figsize=(20, 15))

# Pie Chart for Device Class Distribution
plt.subplot(2, 3, 1)
device_class_counts.plot(kind='pie', autopct='%1.1f%%', startangle=140, colors=sns.color_palette("Set2"))
plt.title('Device Class Distribution', fontsize=16)
plt.ylabel('')  # Hiding the y-label for Pie chart

# Count Plot for Medical Specialty Analysis
plt.subplot(2, 3, 2)
sns.countplot(y='medical_specialty', data=df, order=df['medical_specialty'].value_counts().index, palette="Set2")
plt.title('Medical Specialty Distribution', fontsize=16)
plt.xlabel('Count', fontsize=14)
plt.ylabel('Medical Specialty', fontsize=14)

# Donut Chart for Third Party Review Eligibility
plt.subplot(2, 3, 3)
third_party_review_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=sns.color_palette("coolwarm"), wedgeprops=dict(width=0.3))
plt.title('Third Party Review Eligibility', fontsize=16)
plt.ylabel('')

# Donut Chart for GMP Exemption Status
plt.subplot(2, 3, 4)
gmp_exempt_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=sns.color_palette("coolwarm"), wedgeprops=dict(width=0.3))
plt.title('GMP Exemption Status', fontsize=16)
plt.ylabel('')

# Donut Chart for Implant Flag Distribution
plt.subplot(2, 3, 5)
implant_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=sns.color_palette("coolwarm"), wedgeprops=dict(width=0.3))
plt.title('Implant Flag Distribution', fontsize=16)
plt.ylabel('')

# Donut Chart for Life-Sustaining Flag Distribution
plt.subplot(2, 3, 6)
life_sustain_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=sns.color_palette("coolwarm"), wedgeprops=dict(width=0.3))
plt.title('Life-Sustaining Flag Distribution', fontsize=16)
plt.ylabel('')

# Adjust layout for better spacing and visibility
plt.tight_layout()

# Show the plots
plt.show()
