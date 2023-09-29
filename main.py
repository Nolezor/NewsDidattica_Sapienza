import pandas as pd
import asyncio

import formatter
import scraper
import telegram_bot


original = pd.read_excel("scraped.xlsx", usecols=lambda x: 'Unnamed' not in x)
new = scraper.scrape()

merged = new.merge(original, how="left", on="Titles", indicator=True)
indexes = merged.index[merged['_merge'] == "left_only"].tolist()

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

scraper.save_excel(new, "scraped.xlsx")
