import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('output/twitter_data_on_indian_railways.csv')

# Filter the DataFrame to include only rows where 'is_complaint_true' is 1
df_complaints = df[df['is_complaint_true'] == 1].copy()

# Reset the index of the filtered DataFrame
df_complaints.reset_index(drop=True, inplace=True)
df_complaints.index = df_complaints.index + 1
df_complaints['index'] = df_complaints.index  

# Save the filtered and reindexed DataFrame to a new CSV file
df_complaints.to_csv('output/indian_railways_complaints.csv', index=False)