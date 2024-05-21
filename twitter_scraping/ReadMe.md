## Indian Railways Twitter Data Scraping

This repository contains scripts and tools to scrape Twitter data related to Indian Railways using selenium. The primary goal is to collect and analyze tweets mentioning Indian Railways to gain insights into customer sentiment,  and common issues.

#### Features

* Data Collection: Scrape tweets mentioning indian railways OR @RailMinIndia OR #indianrailways using the CSS selector `div[data-testid='tweetText'` to filter the tweet text only.

* search query: Created search query with filter such as date, search text, minimum replies and retweets for each year.

* Data Storage: Store the scraped data in a csv format for further analysis.

* Scheduling: Year wise scraping data.

* Combine data: Combines each data into a csv and search for complaint keyword into the text.

### Installation

1. Clone the repository:

`https://github.com/RamailoTech/mle-scrapers.git`

2. Navigate to the project directory:

`cd twitter_scraping`

3. Create a virtual environment:

`python3 -m venv venv`

4. Activate the virtual environment:

`source venv/bin/activate`

5. Install dependencies:

`pip install -r requirements.txt`

6. Create .env file and add twitter username and password.

7. Add permission for bash script:

`chmod +x run_scripts.sh`

8. Run the bash script:

`./run_scripts.sh year`

Note: Replace year with the specific year you want to work for. (Eg: 2023)



