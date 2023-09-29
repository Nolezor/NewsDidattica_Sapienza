import scraper


df = scraper.scrape()

scraper.save_excel(df, "scraped.xlsx")
