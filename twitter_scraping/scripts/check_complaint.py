import pandas as pd

# Specify the path to your CSV file
file_path = "output/combined_csv.csv"

# Reading the CSV data from the file path
df = pd.read_csv(file_path)

# Convert all columns to string and handle missing values
df = df.fillna("")  # Replace NaN with empty string
df = df.astype(str)  # Convert all columns to strings

# Concatenating specific columns into one 'text' column
# Temporarily drop the 'index' column if it exists
if "index" in df.columns:
    df["text"] = df.drop("index", axis=1).agg(" ".join, axis=1)
else:
    df["text"] = df.agg(" ".join, axis=1)

# Checking if 'text' contains the word 'complaint' (case insensitive)
df["is_complaint_true"] = df["text"].str.contains("complaint", case=False, na=False)

# Selecting the desired columns for the final output
final_df = df[["index", "text", "is_complaint_true", "date", "year"]]

# Optionally, save the DataFrame to a new CSV file
final_df.to_csv("output/twitter_data_on_indian_railways.csv", index=False)

# Calculate the number of complaints
complaint_count = df["is_complaint_true"].sum()
print(f"Number of complaints: {complaint_count}")
