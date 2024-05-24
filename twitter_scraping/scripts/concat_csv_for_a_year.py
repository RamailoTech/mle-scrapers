import pandas as pd
import os
import sys

def process_csv_files(directory, year):
    # Gather all CSV files from the specified directory for the given year
    files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.csv') and year in f]

    # Load and process each file
    data_frames = []
    for file in files:
        df = pd.read_csv(file)
        df['year'] = year  # Replace the 'year' column with the user-provided year
        data_frames.append(df)

    # Concatenate all DataFrames into one
    combined_df = pd.concat(data_frames)

    # Drop rows where 'text' column is null
    combined_df.dropna(subset=['text'], inplace=True)

    # Filter out entries with less than 5 words in the 'text' column
    combined_df = combined_df[combined_df['text'].str.split().str.len() >= 4]

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

def main():
    # Check if the year argument is provided
    if len(sys.argv) < 2:
        sys.exit(1)

    # Get the year from the command line argument
    year = sys.argv[1]

    directory = "output/year_wise_data_{year}"
    # Call the function to process JSON files with the specified year
    process_csv_files(directory,year)


if __name__ == "__main__":
    main()
