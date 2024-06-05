import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_state_info(url):
    # Fetch the HTML content
    response = requests.get(url)
    if response.status_code != 200:
        return None
    html_content = response.content

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract the state name
    state_name = soup.find('div', class_='page-title').find('span').get_text(strip=True)

    # Extract the "Status Known For" text
    status_text = soup.find('thead').find_all('tr')[0].get_text(strip=True)

    return state_name, status_text

def save_to_csv(data, filename):
    df = pd.DataFrame(data, columns=['State Name', 'Status Known For'])
    df.drop_duplicates(subset=['State Name'], inplace=True)
    df.to_csv(filename, index=False)
    print(f"CSV file has been saved to {filename}")

def main():
    base_url_U = "https://results.eci.gov.in/PcResultGenJune2024/statewiseU"
    base_url_S = "https://results.eci.gov.in/PcResultGenJune2024/statewiseS"
    number_range = range(1, 300)  # Change the range as needed

    all_data = []

    for number in number_range:
        url_U = f"{base_url_U}{number:03d}.htm"
        url_S = f"{base_url_S}{number:03d}.htm"
        
        print(f"Fetching data from {url_U}")
        data_U = fetch_state_info(url_U)
        if data_U:
            all_data.append(data_U)
        else:
            print(f"Skipping {url_U}")
        
        print(f"Fetching data from {url_S}")
        data_S = fetch_state_info(url_S)
        if data_S:
            all_data.append(data_S)
        else:
            print(f"Skipping {url_S}")

    # Save all data to CSV
    save_to_csv(all_data, "state_info.csv")

if __name__ == "__main__":
    main()
