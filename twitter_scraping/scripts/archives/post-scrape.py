from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import getpass
from bs4 import BeautifulSoup

url = "https://www.facebook.com/"
username = input("Enter your username: ")
password = getpass.getpass("Enter your password: ")
chrome_options = Options()
prefs = {
    "profile.managed_default_content_settings.images": 2,
}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=chrome_options
)

driver.get(url)
email_field = driver.find_element(By.XPATH, '//*[@id="email"]')
email_field.send_keys(username)
password_field = driver.find_element(By.XPATH, '//*[@id="pass"]')
password_field.send_keys(password, Keys.ENTER)
time.sleep(10)

post_url = "https://www.facebook.com/search/posts?q=indianrailways"
# hashtag_url = "https://www.facebook.com/hashtag/indianrailways"
driver.get(post_url)
time.sleep(30)

xpath_query = "//div[contains(@class, 'html-div') and not(@aria-label) and not(.//a[@aria-label='Open reel in Reels Viewer'])]"

# Find all div elements based on the defined XPath
div_elements = driver.find_elements(By.XPATH, xpath_query)

# Open a file to write the outputs
with open("div_outerHTML_contents_filtered_post.txt", "w", encoding="utf-8") as file:
    # Iterate over each element to get its content
    for index, div in enumerate(div_elements):
        html_content = div.get_attribute("innerHTML")  # Get innerHTML of the element

        # # Optionally check if the div is displayed before writing (comment out if all divs are needed)
        # # if div.is_displayed():
        # file.write(f"Content of div {index+1} with class 'html-div':\n")
        # file.write(html_content)
        # file.write("\n" + "-" * 40 + "\n")
        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")

        # Find all nested div elements with the style 'text-align: start;'
        target_divs = soup.find_all(
            "div", style=lambda value: value and "text-align: start;" in value
        )

        # Extract and write the text content of each targeted div
        for i, target_div in enumerate(target_divs, 1):
            text_content = target_div.get_text(strip=True)  # Get clean text content
            file.write(f"{text_content}\n")
