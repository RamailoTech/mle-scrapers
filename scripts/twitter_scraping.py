from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import getpass
from dotenv import load_dotenv
import os
import csv
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)

load_dotenv()


def scroll_down(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)


url = "https://x.com/i/flow/login"
# username = input("Enter your username: ")
# password = getpass.getpass("Enter your password: ")
username = os.getenv("username")
password = os.getenv("password")
chrome_options = Options()
# prefs = {
#     "profile.managed_default_content_settings.images": 2,
# }
# chrome_options.add_experimental_option("prefs", prefs)
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
    "@RailMinIndia min_replies:10 since:2024-01-01 -filter:links -filter:replies",
    Keys.ENTER,
)
time.sleep(20)


articles_list = []  # Store each concatenated span text in this list
date_time = []

elements = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='User-Name']")
for element in elements:
    a_tags = element.find_elements(By.CSS_SELECTOR, "a[href*='/status/']")
    for a_tag in a_tags:
        time_elements = a_tag.find_elements(By.TAG_NAME, 'time')
        
        for time_element in time_elements:
            datetime_value = time_element.get_attribute('datetime')
            visible_date = time_element.text
            date_time.append(visible_date)
         



elements = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='tweetText']")
for element in elements:
    spans = element.find_elements(By.TAG_NAME, "span")
    concatenated_spans = " ".join([span.text.strip() for span in spans])
    articles_list.append(concatenated_spans)
    #for time
    



# Write data to CSV after collecting all articles
with open("output/test-twitter-output.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Index", "Text","Time"])  # Adding header row
    for index, (tweet_text, time_text) in enumerate(zip(articles_list, date_time), start=1):
        writer.writerow([index, tweet_text, time_text])
# Close the browser
driver.quit()

