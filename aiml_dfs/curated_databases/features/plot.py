import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load the updated data
df = pd.read_excel('./final_device_features.xlsx', engine='openpyxl')

# Prepare data for plots
device_class_counts = df['device_class'].value_counts()
medical_specialty_counts = df['medical_specialty'].value_counts()
third_party_review_counts = df['third_party_review'].value_counts()
gmp_exempt_counts = df['gmp_exempt_flag'].value_counts()
implant_counts = df['implant_flag'].value_counts()
life_sustain_counts = df['life_sustain_flag'].value_counts()


# Function to create and save individual plots with APA style
def create_and_save_plot_apa(plot_func, title, filename, legend=None, xlabel=None, ylabel=None):
    plt.figure(figsize=(8, 6))
    plt.title(title, fontsize=14, fontstyle='italic')
    plot_func()
    if legend:
        plt.legend(legend)
    if xlabel:
        plt.xlabel(xlabel)
    if ylabel:
        plt.ylabel(ylabel)

    save_path = os.path.join(os.path.expanduser('./initial_plots/'), f'{filename}.png')
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()


# Creating each plot as an independent figure
create_and_save_plot_apa(
    lambda: device_class_counts.plot(kind='pie', autopct='%1.1f%%', startangle=140, colors=sns.color_palette("Set2")),
    'Figure 1: Device Class Distribution',
    'device_class_distribution_apa')

create_and_save_plot_apa(
    lambda: sns.countplot(y='medical_specialty', data=df, order=df['medical_specialty'].value_counts().index, palette="Set2"),
    'Figure 2: Medical Specialty Distribution',
    'medical_specialty_distribution_apa',
    ylabel='Medical Specialty',
    xlabel='Count')

create_and_save_plot_apa(
    lambda: third_party_review_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=sns.color_palette("coolwarm"), wedgeprops=dict(width=0.3)),
    'Figure 3: Third Party Review Eligibility',
    'third_party_review_eligibility_apa')

create_and_save_plot_apa(
    lambda: gmp_exempt_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=sns.color_palette("coolwarm"), wedgeprops=dict(width=0.3)),
    'Figure 4: GMP Exemption Status',
    'gmp_exemption_status_apa')

create_and_save_plot_apa(
    lambda: implant_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=sns.color_palette("coolwarm"), wedgeprops=dict(width=0.3)),
    'Figure 5: Implant Flag Distribution',
    'implant_flag_distribution_apa')

create_and_save_plot_apa(
    lambda: life_sustain_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=sns.color_palette("coolwarm"), wedgeprops=dict(width=0.3)),
    'Figure 6: Life-Sustaining Flag Distribution',
    'life_sustaining_flag_distribution_apa')

# File names of the saved APA style plots
saved_files_apa = [
    'device_class_distribution_apa.png',
    'medical_specialty_distribution_apa.png',
    'third_party_review_eligibility_apa.png',
    'gmp_exemption_status_apa.png',
    'implant_flag_distribution_apa.png',
    'life_sustaining_flag_distribution_apa.png'
]
