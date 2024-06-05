# import pandas as pd

# def count_entries_per_state(csv_filename, output_filename):
#     # Read the CSV file
#     df = pd.read_csv(csv_filename)

#     # Count the number of entries per state
#     state_counts = df['State Name'].value_counts().reset_index()

#     # Rename the columns for better clarity
#     state_counts.columns = ['State Name', 'Count']

#     # Save the results to a new CSV file
#     state_counts.to_csv(output_filename, index=False)
#     print(f"Count of entries per state has been saved to {output_filename}")

# def main():
#     input_csv = 'output/final_combined/combined_sorted_election_results.csv'  # Replace with your actual CSV file path
#     output_csv = 'output/final_combined/counts.csv'  # Output CSV file name

#     count_entries_per_state(input_csv, output_csv)

# if __name__ == "__main__":
#     main()


import pandas as pd

def combine_csv_files(count_csv, status_csv, output_csv):
    # Read the CSV files
    df_count = pd.read_csv(count_csv)
    df_status = pd.read_csv(status_csv)

    # Merge the two DataFrames on 'State Name'
    combined_df = pd.merge(df_count, df_status, on='State Name', how='inner')

    # Remove duplicate state names
    combined_df.drop_duplicates(subset=['State Name'], inplace=True)

    # Save the combined DataFrame to a new CSV file
    combined_df.to_csv(output_csv, index=False)
    print(f"Combined CSV file has been saved to {output_csv}")

def main():
    count_csv = 'state_info.csv'  # Replace with your actual count CSV file path
    status_csv = 'output/final_combined/counts.csv'  # Replace with your actual status CSV file path
    output_csv = 'combined_state_info.csv'  # Output CSV file name

    combine_csv_files(count_csv, status_csv, output_csv)

if __name__ == "__main__":
    main()

