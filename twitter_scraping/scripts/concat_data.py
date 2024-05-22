import pandas as pd
import os

def process_csv_files(directory, year):
    # Gather all CSV files from the specified directory for the given year
    files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('_data.csv') and year in f]

    # Load and process each file
    data_frames = []
    for file in files:
        df = pd.read_csv(file)
        df['year'] = year  # Replace the 'year' column with the user-provided year
        data_frames.append(df)

    # Concatenate all DataFrames into one
    combined_df = pd.concat(data_frames)

    # combined_df = combined_df[combined_df['text'].str.split().str.len() > 5]
    # Remove duplicates based on the 'text' column and keep the first occurrence
    combined_df = combined_df.drop_duplicates(subset=['text'])

    # Select the top 200 rows
    top_200_df = combined_df.head(200)

    # Reset index and adjust index to start from 1
    top_200_df.reset_index(drop=True, inplace=True)
    top_200_df.index += 1
    top_200_df['index'] = top_200_df.index
    print(len(top_200_df))
    # Save the final DataFrame to a new CSV file
    output_path = f"output/year_wise_data/{year}_data.csv"
    top_200_df.to_csv(output_path, index=False)

    return top_200_df

# Usage
year = "2014"
directory = "output/year_wise_data_2014"
process_csv_files(directory, year)
