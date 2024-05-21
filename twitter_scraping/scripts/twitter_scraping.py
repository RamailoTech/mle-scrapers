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
    "2014": "(indian railways OR @RailMinIndia OR #indianrailways) until:2014-12-31 since:2014-01-01 -filter:links -filter:replies",
    "2015": "(indian railways OR @RailMinIndia OR #indianrailways) until:2015-12-31 since:2015-01-01 -filter:links -filter:replies",
    "2016": "(indian railways OR @RailMinIndia OR #indianrailways) until:2016-12-31 since:2016-01-01 -filter:links -filter:replies",
    "2017": "(indian railways OR @RailMinIndia OR #indianrailways) until:2017-12-31 since:2017-01-01 -filter:links -filter:replies",
    "2018": "(indian railways OR @RailMinIndia OR #indianrailways) until:2018-12-31 since:2018-01-01 -filter:links -filter:replies",
    "2019": "(indian railways OR @RailMinIndia OR #indianrailways) min_replies:20 min_retweets:20 until:2019-12-30 since:2019-01-01 -filter:links -filter:replies",
    "2020": "(indian railways OR @RailMinIndia OR #indianrailways) min_replies:20 min_retweets:20 until:2020-12-30 since:2020-01-01 -filter:links -filter:replies",
    "2021": "(indian railways OR @RailMinIndia OR #indianrailways) min_replies:20 min_retweets:20 until:2021-12-30 since:2021-01-01 -filter:links -filter:replies",
    "2022": "(indian railways OR @RailMinIndia OR #indianrailways) min_replies:20 min_retweets:20 until:2022-12-30 since:2022-01-01 -filter:links -filter:replies",
    "2023": "(indian railways OR @RailMinIndia OR #indianrailways) min_replies:20 min_retweets:20 until:2023-12-30 since:2023-01-01 -filter:links -filter:replies",
    "2024": "(indian railways OR @RailMinIndia OR #indianrailways) min_replies:10 min_retweets:20 since:2024-01-01 -filter:links -filter:replies",
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
    time.sleep(10)
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

    articles_list = []  # Store each concatenated span text in this list
    date_time = []  # store date for each posts

    # 50 scrolls
    for _ in range(50):
        elements = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='User-Name']")
        for element in elements:
            if len(date_time) >= 200:  # Check if already collected 200 datetimes
                break
            a_tags = element.find_elements(By.CSS_SELECTOR, "a[href*='/status/']")
            for a_tag in a_tags:
                time_elements = a_tag.find_elements(By.TAG_NAME, "time")

                for time_element in time_elements:
                    datetime_value = time_element.get_attribute("datetime")
                    visible_date = time_element.text
                    date_time.append(visible_date)
                    if (
                        len(date_time) >= 200
                    ):  # Check if already collected 200 datetimes
                        break

        elements = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='tweetText']")
        for element in elements:
            if len(articles_list) >= 200:  # Check if already collected 200 datetimes
                break
            spans = element.find_elements(By.TAG_NAME, "span")
            concatenated_spans = " ".join([span.text.strip() for span in spans])
            articles_list.append(concatenated_spans)
            if len(articles_list) >= 200:  # Check if already collected 200 datetimes
                break
        scroll_down(driver)

    # Write data to CSV after collecting all tweets
    with open(
        f"output/year_wise_data/{year}_data.csv", "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.writer(file)
        writer.writerow(["index", "text", "date", "year"])  # Adding header row
        for index, (tweet_text, time_text) in enumerate(
            zip(articles_list, date_time), start=1
        ):
            writer.writerow([index, tweet_text, time_text, year])
    # Close the browser
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
