import pandas as pd
import asyncio

import formatter
import scraper
import telegram_bot


# Get the 2 dataframe to compare (this part check if there is any news)
# The lambda function can be removed by changing the way the dataframe is saved in scraper.py
original = pd.read_excel("scraped.xlsx", usecols=lambda x: 'Unnamed' not in x)
new = scraper.scrape()

merged = new.merge(original, how="left", on="Titles", indicator=True)  # Check differences in the 2 dataframes
indexes = merged.index[merged['_merge'] == "left_only"].tolist()  # Gets the index of the changes

for idx in indexes:
    message = ""
    # TODO: format Text
    title = new['Titles'][idx]
    content = new['Contents'][idx]
    link = new['Links'][idx]
    message += formatter.format_title(title)
    if len(content) > 0:
        message += formatter.format_content(content)
    if len(link) > 0:
        message += formatter.format_links(link)
    message += "\n"
    asyncio.run(telegram_bot.send_message(message))

# Updates the Excel used to check for changes
scraper.save_excel(new, "scraped.xlsx")
