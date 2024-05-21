import playwright
from playwright.sync_api import sync_playwright

username = input("Enter your username: ")
password = input("Enter your password: ")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=100)
    page = browser.new_page()
    page.goto("https://www.facebook.com/")
    page.fill('input#email',username)
    page.fill('input#pass',password)
    page.click('button[type=submit]')