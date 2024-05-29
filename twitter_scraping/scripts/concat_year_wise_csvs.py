import pandas as pd
import os
import re


def clean_text(text):
    if pd.isnull(text):
        return text  # Return as is if text is NaN
    text = text.strip()  # Remove leading and trailing whitespace
    text = re.sub(r"\s+", " ", text)  # Replace multiple spaces with a single space
    # Add more cleaning rules here if necessary
    return text


def main():
    # Specify the directory containing the CSV files
    directory = "output/year_wise_data"

    # List all CSV files in the directory
    csv_files = [
        os.path.join(directory, file)
        for file in os.listdir(directory)
        if file.endswith(".csv")
    ]

    # Read each CSV file and store them in a list
    dataframes = [pd.read_csv(file) for file in csv_files]

    # Concatenate all the DataFrames in the list
    combined_df = pd.concat(dataframes, ignore_index=True)
    # clean the text column
    combined_df["text"] = combined_df["text"].apply(clean_text)
    # Extract year from 'Date' and create a new column
    combined_df["year"] = combined_df["year"]

    # Sort the DataFrame by 'Year' in descending order
    combined_df.sort_values(by="year", ascending=False, inplace=True)

    # Reset the index to start from 1
    combined_df.reset_index(drop=True, inplace=True)
    combined_df.index = combined_df.index + 1
    combined_df["index"] = (
        combined_df.index
    )  # Update the 'Index' column to reflect the new ordering

    output_path = "output/final_data/twitter_railway_data_validated.xlsx"
    combined_df.to_excel(output_path, index=False, engine="openpyxl")


if __name__ == "__main__":
    main()
