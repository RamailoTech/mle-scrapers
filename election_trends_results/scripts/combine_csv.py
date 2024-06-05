import os
import pandas as pd

def combine_and_sort_csv(input_folder, output_file):
    all_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]
    combined_df = pd.DataFrame()

    for file in all_files:
        file_path = os.path.join(input_folder, file)
        df = pd.read_csv(file_path)
        combined_df = pd.concat([combined_df, df], ignore_index=True)
    
    sorted_df = combined_df.sort_values(by='State Name')
    
    sorted_df.to_csv(output_file, index=False)
    print(f"Combined and sorted CSV file has been saved to {output_file}")
    unique_states = sorted_df['State Name'].nunique()
    print(f"Number of unique state names: {unique_states}")

def main():
    input_folder = 'output/state_wise_csv'  # Folder containing the CSV files
    output_file = 'combined_sorted_election_results.csv'  # Output CSV file name

    combine_and_sort_csv(input_folder, output_file)

if __name__ == "__main__":
    main()
