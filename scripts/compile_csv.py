import pandas as pd

# Specify the path to your CSV file
file_path = 'output.csv'  # Replace 'path_to_your_file.csv' with the actual path to your CSV file

# Reading the CSV data from the file path
df = pd.read_csv(file_path)

# Concatenating all columns into one 'text' column
df['text'] = df.fillna('').agg(' '.join, axis=1)

# Adding an ID column starting from 1
df['id'] = range(1, len(df) + 1)

# Checking if 'text' contains the word 'complaint' (case insensitive)
df['is_complaint_true'] = df['text'].str.contains('complaint', case=False, na=False)

# Selecting the desired columns for the final output
final_df = df[['id', 'text', 'is_complaint_true']]

# Optionally, save the DataFrame to a new CSV file
final_df.to_csv('final_csv.csv', index=False)


complaint_count = df['is_complaint_true'].sum()
print(f"Number of complaints: {complaint_count}")
