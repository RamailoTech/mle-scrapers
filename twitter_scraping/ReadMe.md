## Indian Railways Twitter Data Scraping

This repository contains scripts and tools to scrape Twitter data related to Indian Railways using selenium. The primary goal is to collect and analyze tweets mentioning Indian Railways to gain insights into customer sentiment,  and common issues.

#### Features

* Data Collection: Scrape tweets mentioning indian railways OR @RailMinIndia OR #indianrailways using the CSS selector `div[data-testid='tweetText'` to filter the tweet text only. Also to ensure that no tweets are repeating, id of each tweets are also selected.

* search query: Created search query with filter such as date, search text for each year.

* Data Storage: Store the scraped data in a csv format for further analysis.

* Scheduling: Year wise scraping data.

* Combine data: Combines each data into a csv and search for complaint keyword into the text.


#### Steps involved during scraping

* Used search filter such as `(#indianrailways) until:2014-12-30 since:2014-01-01` with three different keywords for each year. (keywords: RailMinIndia, indianrailways, #indianrailways)

* Scrape the web contents for each search results for each year.

* Concatenate the scraped search results for three different keywords and generate final csv by removing duplicates.

* Used gpt-3.5 turbo to classify if the text data was complaint or not.
    Sample prompt:
    ```Is the following text describing a complaint about indian railway services. Answer 1 if true and 0 if not. Answer only 1 or 0, nothing else.
    Example 1:
    Mr @narendramodi will let people die/substandard service & so on  on Indian  Railways but won't privatise .

    Output: 1
    
    Example 2:
    Happy 52nd Birthday to Fastest Rajdhani Express in Indian Railways ""The Mumbai Rajdhani"" 
    @WesternRly
    #indianrailways
    
    Output: 0```


* Used gpt-3.5 turbo to classify if if it belongs to one of the following categories:
    1. delay
    2. crowding
    3. expensive
    4. derail
    5. hygiene
    6. management

Sample prompt:

```You are a multi-class classification model. You will be given a complaint about services in the railways. Classify the given compaint into the             following four categories:
        delay: The complaint is about delays and punctuality issues in the train schedules.
        crowding: The complaint is about overcrowding in the trains. 
        expensive: The complaint is about the railways having become expensive and unaffordable. 
        derail: The complaint is about trains derailing. 
        hygiene: The complaint concerns the cleanliness and sanitary conditions of the trains.
        management: The complaint addresses issues related to the overall administration and organization of the train services. Also inculdes reduction in the number of sleeper and 3AC coaches, which disproportionately affects poor and middle-class passengers.
 
        Answer 1 if it falls into the given category 0 if not. Answer only 1 or 0, nothing else. Also, check the synonyms of the given categories. Provide the output in JSON format.
                Note: The given complaint might fall in all/some/any category.

        Sample output format:
        {
            "delay":1,
            "crowding": 1,
            "expensive": 0,
            "derail":0,
            "hygiene":0,
            "management":1
        }

        Example 1:
        #indianrailway   #IndianRailways  tejas express (bom - goa) What a magnificent train but what a poor schedule.. express train waiting at each and every station. 2 hour delay. poor service - Indian  Railways .

        Output:
        {
            "delay":1,
            "crowding": 0,
            "expensive": 0,
            "derail":0,
            "hygiene":0,
            "management":1
        }

        Example 2:
        Big punctuality fraud is going on in Indian  Railways . This practice of bogus punctuality data must be stopped. Use technology and stop manipulation. Indian  #Railways  runs a monopoly and has no regulator. Accidents occur. Premium fares, dynamic pricing. Anything for poor?

        Output:
        {
            "delay":1,
            "crowding": 1,
            "expensive": 0,
            "derail":0,
            "hygiene":0,
            "management":0
        }```

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



