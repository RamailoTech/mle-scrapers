import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def fetch_table_data(url):
    # Fetch the HTML content
    response = requests.get(url)
    if response.status_code != 200:
        return None
    html_content = response.content

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract the state name
    state_name = soup.find('div', class_='page-title').find('span').get_text(strip=True)

    # Extract table rows
    rows = soup.find_all('tr')

    data = []
    columns = ['Constituency', 'Const. No.', 'Leading Candidate', 'Leading Party', 'Trailing Candidate', 'Trailing Party', 'Margin', 'Status', 'State Name']

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
            cleaned_row = [row_data[0], row_data[1], row_data[2], row_data[3], row_data[6], row_data[7], row_data[10], row_data[11], state_name]
            data.append(cleaned_row)

    if data:
        return columns, data
    return None

def save_to_csv(headers, rows, filename):
    df = pd.DataFrame(rows, columns=headers)
    # Ensure the results directory exists
    if not os.path.exists('results'):
        os.makedirs('results')
    file_path = os.path.join('results', filename)
    df.to_csv(file_path, index=False)
    print(f"CSV file has been saved to {file_path}")

def main():
    base_url_U = "https://results.eci.gov.in/PcResultGenJune2024/statewiseU"
    base_url_S = "https://results.eci.gov.in/PcResultGenJune2024/statewiseS"
    number_range = range(1, 300)  # Change the range as needed

    for number in number_range:
        url_U = f"{base_url_U}{number:03d}.htm"
        url_S = f"{base_url_S}{number:03d}.htm"
        
        print(f"Fetching data from {url_U}")
        data_U = fetch_table_data(url_U)
        if data_U:
            headers, rows = data_U
            save_to_csv(headers, rows, f"statewiseU{number:03d}.csv")
        else:
            print(f"Skipping {url_U}")
        
        print(f"Fetching data from {url_S}")
        data_S = fetch_table_data(url_S)
        if data_S:
            headers, rows = data_S
            save_to_csv(headers, rows, f"statewiseS{number:03d}.csv")
        else:
            print(f"Skipping {url_S}")

if __name__ == "__main__":
    main()
