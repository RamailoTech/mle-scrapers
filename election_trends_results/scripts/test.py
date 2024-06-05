from bs4 import BeautifulSoup
import requests
import pandas as pd

# URL to fetch the HTML content
url = 'https://results.eci.gov.in/PcResultGenJune2024/statewiseS012.htm'

# Fetch the HTML content
response = requests.get(url)
html_content = response.content
# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Extract table rows
rows = soup.find_all('tr')

# Prepare data for the DataFrame
data = []
columns = ['Constituency', 'Const. No.', 'Leading Candidate', 'Leading Party', 'Trailing Candidate', 'Trailing Party', 'Margin', 'Status']

for row in rows[2:]:  # Skipping the header rows
    cols = row.find_all('td')
    row_data = []
    for col in cols:
        if col.find('div', class_='tooltip'):
            col.find('div', class_='tooltip').decompose()  # Remove the tooltip div
        nested_table = col.find('table')
        if nested_table:
            nested_td = nested_table.find_all('td')[0]
            row_data.append(nested_td.get_text(strip=True))
        else:
            text = col.get_text(strip=True)
            if text:  # Skip empty text
                row_data.append(text)
    # Extract only the necessary columns from the row data
    if len(row_data) == 12:
        cleaned_row = [row_data[0], row_data[1], row_data[2], row_data[3], row_data[6], row_data[7], row_data[10], row_data[11]]
        data.append(cleaned_row)

# Create DataFrame
df = pd.DataFrame(data, columns=columns)

# Save DataFrame to CSV
csv_path = 'election_results_single.csv'
df.to_csv(csv_path, index=False)

print(f"CSV file has been saved to {csv_path}")
