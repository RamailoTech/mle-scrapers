from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from dotenv import load_dotenv
import os
import csv
import sys


load_dotenv()
username = os.getenv("TWITTER_USERNAME")
password = os.getenv("TWITTER_PASSWORD")


search_queries = {
    "2014": "(@RailMinIndia) until:2014-12-30 since:2014-01-01",
    "2015": "(@RailMinIndia) until:2015-12-30 since:2015-01-01",
    "2016": "(@RailMinIndia) until:2016-12-30 since:2016-01-01",
    "2017": "(@RailMinIndia) until:2017-12-30 since:2017-01-01",
    "2018": "(@RailMinIndia) until:2018-12-30 since:2018-01-01",
    "2019": "(@RailMinIndia) until:2019-12-30 since:2019-01-01",
    "2024": "(#indianrailways) since:2024-01-01",
}


def scroll_down(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)


def get_tweet_for_year(year):
    # Get search query
    search_query = search_queries.get(year)
    if not search_query:
        raise ValueError("No search query available for the specified year")

    url = "https://x.com/i/flow/login"

    chrome_options = Options()
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options
    )

    driver.get(url)
    time.sleep(10)
    email_field = driver.find_element(
        By.XPATH,
        '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[4]/label/div/div[2]/div/input',
    )
    email_field.send_keys(username)

    next_button = driver.find_element(
        By.XPATH,
        '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/button[2]',
    )
    next_button.click()
    time.sleep(20)
    password_field = driver.find_element(
        By.XPATH,
        '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input',
    )
    password_field.send_keys(password)
    time.sleep(10)
    login_button = driver.find_element(
        By.XPATH,
        '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/button',
    )
    login_button.click()
    # Maximize the window
    driver.maximize_window()

    time.sleep(15)
    # after login

    search_button = driver.find_element(
        By.XPATH,
        '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/form/div[1]/div/div/div/div/div[2]/div/input',
    )
    search_button.send_keys(
        search_query,
        Keys.ENTER,
    )
    time.sleep(20)

    # tweet_set = set() # Store each concatenated span text in this list
    tweet_dict = {}
    # 50 scrolls
    for i in range(30):
        print("scroll count", i)
        print("tweet counts:", len(tweet_dict))
        elements = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='tweetText']")
        for element in elements:
            # Get the value of the 'id' attribute
            element_id = element.get_attribute("id")
            # print(element_id)
            # Get the text content of the element
            element_text = element.text
            # tweet_set.add(element_text)
            tweet_dict[element_id] = element_text
            if len(tweet_dict) > 200:
                break
        scroll_down(driver)

    # Write data to CSV after collecting all tweets
    # Set the directory path based on the year
    directory_path = f"output/year_wise_data_{year}"

    # Check if the directory exists, and if not, create it
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    # Path to the CSV file
    file_path = f"{directory_path}/{year}_data.csv"
    with open(file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["index", "text", "year"])  # Corrected header row
        for index, (tweet_id, tweet_text) in enumerate(tweet_dict.items(), start=1):
            writer.writerow([index, tweet_text, year])

    driver.quit()


def main():
    # Check if the year argument is provided
    if len(sys.argv) < 2:
        sys.exit(1)

    # Get the year from the command line argument
    year = sys.argv[1]

    # Call the function to process JSON files with the specified year
    get_tweet_for_year(year)


if __name__ == "__main__":
    main()
