# Import necessary libraries
import numpy as np               # Used for numerical computations
import pandas as pd              # Used for handling and analyzing data in DataFrames
import matplotlib.pyplot as plt   # Used for creating visualizations
from datetime import datetime     # Used for working with dates

# Load dataset from a CSV file
worldometer_df = pd.read_csv('worldometer_snapshots_April18_to_May18.csv')

# Display the first few rows of the dataset
worldometer_df

# Define the country of interest (in this case, "USA")
country_name = "USA"

# Extract the data for the specified country ("USA")
country_df = worldometer_df.loc[worldometer_df['Country'] == country_name, :].reset_index(drop=True)
country_df

# Select the data corresponding to a specific date (May 18, 2020)
selected_date = datetime.strptime('18/05/2020', '%d/%m/%Y')

# Filter the dataset to include only rows from the selected date
selected_date_df = worldometer_df.loc[worldometer_df['Date'] == selected_date.strftime('%Y-%m-%d'), :].reset_index(drop=True)
selected_date_df

# Define the last date for the analysis (May 18, 2020)
last_date = datetime.strptime('18/05/2020', '%d/%m/%Y')

# Extract the data corresponding to the last date
last_date_df = worldometer_df.loc[worldometer_df['Date'] == last_date.strftime('%Y-%m-%d'), :].reset_index(drop=True)
last_date_df

# Calculate the Case Fatality Ratio (CFR) for each country on the last date
last_date_df['Case Fatality Ratio'] = last_date_df['Total Deaths'] / last_date_df['Total Cases']

# Plot a histogram of death rates (CFR) for all countries
plt.figure(figsize=(12,8))
plt.hist(100 * np.array(last_date_df['Case Fatality Ratio']), bins=np.arange(35))  # Convert CFR to percentage
plt.xlabel('Death Rate (%)', fontsize=16)
plt.ylabel('Number of Countries', fontsize=16)
plt.title('Histogram of Death Rates for various Countries', fontsize=18)
plt.show()

# Define the minimum number of cases for filtering greatly affected countries
min_number_of_cases = 1000

# Filter the dataset to include only countries with more than 1000 total cases
greatly_affected_df = last_date_df.loc[last_date_df['Total Cases'] > min_number_of_cases,:]

# Plot a histogram of death rates for countries with more than 1000 cases
plt.figure(figsize=(12,8))
plt.hist(100 * np.array(greatly_affected_df['Case Fatality Ratio']), bins=np.arange(35))  # Convert CFR to percentage
plt.xlabel('Death Rate (%)', fontsize=16)
plt.ylabel('Number of Countries', fontsize=16)
plt.title('Histogram of Death Rates for various Countries', fontsize=18)
plt.show()

# Calculate the number of tests per positive case for each country on the last date
last_date_df['Num Tests per Positive Case'] = last_date_df['Total Tests'] / last_date_df['Total Cases']

# Re-filter the dataset for countries with more than 1000 total cases
greatly_affected_df = last_date_df.loc[last_date_df['Total Cases'] > min_number_of_cases,:]

# Set the limit for the x-axis (maximum value for tests per positive case)
x_axis_limit = 80

# Prepare data for plotting a scatter plot
death_rate_percent = 100 * np.array(greatly_affected_df['Case Fatality Ratio'])      # Death rate percentage
num_test_per_positive = np.array(greatly_affected_df['Num Tests per Positive Case'])  # Number of tests per positive case
num_test_per_positive[num_test_per_positive > x_axis_limit] = x_axis_limit           # Cap the tests per positive case to the limit
total_num_deaths = np.array(greatly_affected_df['Total Deaths'])                    # Total number of deaths
population = np.array(greatly_affected_df['Population'])                            # Population of each country

# Plot a scatter plot to visualize the relationship between testing quality and death rate
plt.figure(figsize=(16,12))
plt.scatter(x=num_test_per_positive, y=death_rate_percent, 
            s=0.5*np.power(np.log(1+population),2),   # Marker size based on population (scaled logarithmically)
            c=np.log10(1+total_num_deaths))           # Marker color based on total deaths (scaled logarithmically)
plt.colorbar()
plt.ylabel('Death Rate (%)', fontsize=16)
plt.xlabel('Number of Tests per Positive Case', fontsize=16)
plt.title('Death Rate as function of Testing Quality', fontsize=18)
plt.xlim(-1, x_axis_limit + 12)
plt.ylim(-0.2, 17)

# List of specific countries to highlight on the plot
countries_to_display = ['USA', 'Russia', 'Spain', 'Brazil', 'UK', 'Italy', 'France', 
                        'Germany', 'India', 'Canada', 'Belgium', 'Mexico', 'Netherlands', 
                        'Sweden', 'Portugal', 'UAE', 'Poland', 'Indonesia', 'Romania', 
                        'Thailand','Kyrgyzstan','El Salvador', 'S. Korea', 
                        'Denmark', 'Serbia', 'Norway', 'Algeria', 'Bahrain','Slovenia',
                        'Greece','Cuba','Hong Kong','Lithuania', 'Australia', 'Morocco', 
                        'Malaysia', 'Nigeria', 'Moldova', 'Ghana', 'Armenia', 'Bolivia', 
                        'Iraq', 'Hungary', 'Cameroon', 'Azerbaijan']

# Add the names of specific countries to the scatter plot
for country_name in countries_to_display:
    country_index = greatly_affected_df.index[greatly_affected_df['Country'] == country_name]
    plt.text(x=num_test_per_positive[country_index] + 0.5,  # Shift x-position slightly for readability
             y=death_rate_percent[country_index] + 0.2,     # Shift y-position slightly for readability
             s=country_name, fontsize=10)
plt.show()

# Define a threshold for "good testing" (number of tests per positive case > 50)
good_testing_threshold = 50

# Filter the dataset to include only countries with good testing
good_testing_df = greatly_affected_df.loc[greatly_affected_df['Num Tests per Positive Case'] > good_testing_threshold,:]

# Calculate the estimated death rate for countries with good testing
estimated_death_rate_percent = 100 * good_testing_df['Total Deaths'].sum() / good_testing_df['Total Cases'].sum()

# Print the death rate for countries with good testing
print('Death rate only for "good testing countries" is %.2f%s' %(estimated_death_rate_percent,'%'))
