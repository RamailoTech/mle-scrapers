import pandas as pd


df = pd.read_csv("output/twitter_railway_data.csv")


year_counts = df['year'].value_counts()


year_counts = df['year'].value_counts().sort_index()
print(year_counts)
