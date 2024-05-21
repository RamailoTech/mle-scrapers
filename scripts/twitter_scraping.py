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

# Find all articles on the page
elements = driver.find_elements(By.CLASS_NAME, "css-175oi2r")
for element in elements:
    articles = element.find_elements(By.CSS_SELECTOR, "article[data-testid='tweet']")
    for article in articles:
        spans = article.find_elements(By.TAG_NAME, "span")
        concatenated_spans = " ".join([span.text.strip() for span in spans])
        print()
        articles_list.append(concatenated_spans)

# Write data to CSV after collecting all articles
with open("output/test-twitter-output.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Index", "Text"])  # Adding header row
    for index, article_text in enumerate(articles_list, 1):
        writer.writerow([index, article_text])

# Close the browser
driver.quit()

# # Open a CSV file to write the data directly
# with open("output.csv", "w", newline="", encoding="utf-8") as file:
#     max_spans = 6
#     fieldnames = [f"span{i + 1}" for i in range(max_spans)]
#     writer = csv.DictWriter(file, fieldnames=fieldnames)
#     writer.writeheader()
#     articles= {}
#     #list of dict
#     #dump at last
#     total_articles = 0
#     for i in range(15):
#         print("Loop", i)
#         elements = driver.find_elements(By.CLASS_NAME, "css-175oi2r")
#         for element_index in range(len(elements)):
#             # Re-find element to prevent stale reference
#             element = driver.find_elements(By.CLASS_NAME, "css-175oi2r")[element_index]
#             articles = element.find_elements(
#                 By.CSS_SELECTOR, "article[data-testid='tweetText']"
#             )
#             for article_index in range(len(articles)):
#                 # Re-find article to prevent stale reference
#                 article = element.find_elements(
#                     By.CSS_SELECTOR, "article[data-testid='tweetText']"
#                 )[article_index]
#                 # if total_articles >= 10:
#                 #     break  # Stop processing if we have reached 50 articles
#                 article_dict = {}
#                 spans = article.find_elements(By.TAG_NAME, "span")
#                 for span_index, span in enumerate(spans[:6]):
#                     if span_index >= max_spans:
#                         break
#                     column_name = f"span{span_index + 1}"
#                     article_dict[column_name] = span.text

#                 if article_dict:
#                     print(article_dict)
#                     writer.writerow(article_dict)
#                     total_articles += 1

#         scroll_down(driver)

# # Close the browser
# driver.quit()


# # Open a CSV file to write the data directly
# with open('output.csv', 'w', newline='', encoding='utf-8') as file:
#     max_spans = 6
#     fieldnames = [f'span{i + 1}' for i in range(max_spans)]
#     writer = csv.DictWriter(file, fieldnames=fieldnames)
#     writer.writeheader()

#     total_articles = 0
#     last_height = driver.execute_script("return document.body.scrollHeight")

#     # while total_articles < 50:
#     for _ in range(10):
#         elements = driver.find_elements(By.CLASS_NAME, 'css-175oi2r')
#         for element_index, element in enumerate(elements):
#             articles = element.find_elements(By.TAG_NAME, "article")
#             for article_index, article in enumerate(articles):
#                 if total_articles >= 50:
#                     break  # Stop processing if we have reached 50 articles
#                 article_dict = {}
#                 spans = article.find_elements(By.TAG_NAME, "span")
#                 for span_index, span in enumerate(spans[:6]):
#                     if span_index >= max_spans:
#                         break
#                     column_name = f'span{span_index + 1}'
#                     article_dict[column_name] = span.text

#                 if article_dict:
#                     writer.writerow(article_dict)
#                     total_articles += 1

#         scroll_down(driver)

# # Close the browser
# driver.quit()

# # Find all elements with the class name 'css-175oi2r'
# elements = driver.find_elements(By.CLASS_NAME, "css-175oi2r")

# # Open a CSV file to write the data directly
# with open('output.csv', 'w', newline='', encoding='utf-8') as file:
#     max_spans = 6
#     fieldnames = [f'span{i + 1}' for i in range(max_spans)]
#     writer = csv.DictWriter(file, fieldnames=fieldnames)
#     writer.writeheader()

#     total_articles = 0
#     seen_articles = set()  # To track processed articles

#     while total_articles < 50:
#         elements = driver.find_elements(By.CLASS_NAME, 'css-175oi2r')
#         for element_index, element in enumerate(elements):
#             articles = element.find_elements(By.TAG_NAME, "article")
#             for article_index, article in enumerate(articles):
#                 try:
#                     # Generate a unique key for each article based on its text content
#                     article_key = hash(article.text)
#                     if article_key in seen_articles:
#                         continue  # Skip this article if it has been processed
#                     seen_articles.add(article_key)

#                     article_dict = {}
#                     spans = article.find_elements(By.TAG_NAME, "span")
#                     for span_index, span in enumerate(spans[:6]):
#                         if span_index >= max_spans:
#                             break
#                         column_name = f'span{span_index + 1}'
#                         article_dict[column_name] = span.text.strip()

#                     if article_dict:
#                         writer.writerow(article_dict)
#                         total_articles += 1
#                         if total_articles >= 50:
#                             break  # Stop processing if we have reached 50 articles

#                 except StaleElementReferenceException:
#                     # Handle cases where the page structure changes during scraping
#                     continue

#         # Scroll down and wait for new content to load
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         driver.implicitly_wait(5)  # adjust based on actual page response time

# # Close the browser
# driver.quit()


# validations
# 1. 150 tweets
#
