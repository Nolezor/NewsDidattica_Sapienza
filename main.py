import os
import sys
import asyncio
import logging
import datetime
import pandas as pd

import scraper
import telegram_bot

# Exit codes
NO_NEW_UPDATES = 0
NETWORK_ERROR = 1
DATA_ERROR = 2

if not logging.getLogger().hasHandlers():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

logger = logging.getLogger('news_didattica_main')


def main():
    """Main function that orchestrates the news scraping and notification process.
    
    The function performs the following operations:
    1. Scrapes the Physics department's News Didattica page
    2. Compares new data with previously stored data
    3. Identifies new updates
    4. Saves the current state for future comparison
    5. Sends new updates to a Telegram channel
    
    Returns:
        int: Exit code indicating success (0) or specific error types
    """
    try:
        logger.info("Starting News Didattica Bot")
        
        logger.info("Fetching current data from website")
        now_data = scraper.scrape()
        
        if now_data.empty:
            logger.error("Failed to retrieve data from the website")
            return NETWORK_ERROR
        
        excel_path = os.path.join(sys.path[0], "scraped.xlsx")
        
        if os.path.exists(excel_path):
            try:
                logger.info(f"Loading previous data from {excel_path}")
                old_data = pd.read_excel(excel_path)
                
                logger.info("Comparing current data with previous data")
                merged = now_data.merge(old_data, how="left", on="Contents", indicator=True)
                indexes = merged.index[merged['_merge'] == "left_only"].tolist()
                
                new = now_data.iloc[indexes]
                logger.info(f"Found {len(new)} new updates")
                
            except Exception as e:
                logger.error(f"Error processing previous data: {str(e)}")
                logger.info("Treating this as first run due to error")
                new = now_data
        else:
            logger.info("First run detected - all items will be considered new")
            new = now_data
        
        if len(new) == 0:
            logger.info(f"No new updates found at {datetime.datetime.now()}")
            return NO_NEW_UPDATES
        
        try:
            logger.info(f"Saving current data to {excel_path}")
            scraper.save_excel(now_data, excel_path)
        except Exception as e:
            logger.error(f"Error saving data: {str(e)}")
        
        success_count = 0
        for index, new_data in enumerate(new["Contents"]):
            try:
                logger.info(f"Sending update {index+1}/{len(new)} to Telegram")
                success = asyncio.run(telegram_bot.send_message(new_data))
                if success:
                    success_count += 1
                if index < len(new) - 1:
                    asyncio.run(asyncio.sleep(1))
            except Exception as e:
                logger.error(f"Error sending message: {str(e)}")
        
        logger.info(f"Successfully sent {success_count}/{len(new)} updates")
        return 0
        
    except Exception as e:
        logger.error(f"Unexpected error in main process: {str(e)}")
        return DATA_ERROR


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
