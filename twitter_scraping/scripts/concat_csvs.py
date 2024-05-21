import pandas as pd
import os

# Specify the directory containing the CSV files
directory = 'output/year_wise_data'

# List all CSV files in the directory
csv_files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.csv')]

# Read each CSV file and store them in a list
dataframes = [pd.read_csv(file) for file in csv_files]

# Concatenate all the DataFrames in the list
combined_df = pd.concat(dataframes, ignore_index=True)


# Extract year from 'Date' and create a new column
combined_df['year'] = combined_df['year']

# Sort the DataFrame by 'Year' in descending order
combined_df.sort_values(by='year', ascending=False, inplace=True)

# Reset the index to start from 1
combined_df.reset_index(drop=True, inplace=True)
combined_df.index = combined_df.index + 1
combined_df['index'] = combined_df.index  # Update the 'Index' column to reflect the new ordering

# Save the DataFrame to a new CSV file
output_path = 'output/combined_csv.csv'
combined_df.to_csv(output_path, index=False)
