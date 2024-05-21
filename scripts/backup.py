# Open a CSV file to write the data directly
with open('output.csv', 'w', newline='', encoding='utf-8') as file:
    max_spans = 6
    fieldnames = [f'span{i + 1}' for i in range(max_spans)]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

    total_articles = 0
    seen_articles = set()  # To track processed articles

    # while total_articles < 50:
    for _ in range(5): 
        elements = driver.find_elements(By.CLASS_NAME, 'css-175oi2r')
        for element_index, element in enumerate(elements):
            articles = element.find_elements(By.TAG_NAME, "article")
            for article_index, article in enumerate(articles):
                try:
                    # Generate a unique key for each article based on its text content
                    article_key = hash(article.text)
                    if article_key in seen_articles:
                        continue  # Skip this article if it has been processed
                    seen_articles.add(article_key)

                    article_dict = {}
                    spans = article.find_elements(By.TAG_NAME, "span")
                    for span_index, span in enumerate(spans[:6]):
                        if span_index >= max_spans:
                            break
                        column_name = f'span{span_index + 1}'
                        article_dict[column_name] = span.text.strip()

                    if article_dict:
                        writer.writerow(article_dict)
                        total_articles += 1
                        if total_articles >= 50:
                            break  # Stop processing if we have reached 50 articles

                except StaleElementReferenceException:
                    # Handle cases where the page structure changes during scraping
                    continue

        # Scroll down and wait for new content to load
        scroll_down(driver)   # adjust based on actual page response time

# Close the browser
driver.quit()


