import requests
import pandas as pd
import logging
import sys

from bs4 import BeautifulSoup
from markdownify import markdownify as md
from requests.exceptions import RequestException, Timeout, ConnectionError

# Configure basic logging
if not logging.getLogger().hasHandlers():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

logger = logging.getLogger('news_didattica_scraper')


def scrape():
    """Scrape the Sapienza Physics department News Didattica page.
    
    Returns:
        pd.DataFrame: DataFrame containing news items with 'Contents' column,
                      or empty DataFrame if scraping fails
    """
    URL = "https://www.phys.uniroma1.it/it/news-didattica"
    
    try:
        # Establish a connection to the site with timeout
        logger.info(f"Attempting to fetch data from {URL}")
        page = requests.get(URL, timeout=30)  # 30 seconds timeout
        
        # Check if the request was successful
        page.raise_for_status()
        
        # Obtain all the html from the site
        soup = BeautifulSoup(page.content, "html.parser")

        # Every single update is part of a list and every element of the list has the class "views_row"
        result = soup.find("div", class_="item-list")
        if not result:
            logger.error("Could not find the item-list div on the page. The website structure might have changed.")
            return pd.DataFrame(columns=["Contents"])  # Return empty DataFrame
            
        result = result.find_all("li")
        if not result:
            logger.error("No list items found within the item-list div. The website structure might have changed.")
            return pd.DataFrame(columns=["Contents"])  # Return empty DataFrame
        
        logger.info(f"Successfully fetched {len(result)} items from the website")
        
        for idx, element in enumerate(result):
            # List all the element in their html format and convert them to markdown (standardize for MarkdownV2)
            result[idx] = md(str(element).replace("<li>", "").replace("</li>", "").strip(), autolinks=False)
            
        # Create a dataframe with the data
        df = pd.DataFrame(result, columns=["Contents"])
        return df
        
    except Timeout:
        logger.error(f"Request to {URL} timed out. The server might be slow or unresponsive.")
    except ConnectionError:
        logger.error(f"Failed to connect to {URL}. Check your internet connection or the website might be down.")
    except RequestException as e:
        logger.error(f"Error during request to {URL}: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error during scraping: {str(e)}")
    
    # Return empty DataFrame in case of any error
    return pd.DataFrame(columns=["Contents"])


def save_excel(df, name):
    """Save a DataFrame to an Excel file.
    
    Args:
        df (pd.DataFrame): DataFrame to save
        name (str): Path to the output Excel file
        
    Raises:
        Exception: If saving fails, the exception is logged and re-raised
    """
    try:
        df.to_excel(name)
        logger.info(f"Successfully saved data to {name}")
    except Exception as e:
        logger.error(f"Error saving data to {name}: {str(e)}")
        raise  # Re-raise the exception after logging


if __name__ == "__main__":
    scraped_data = scrape()
    print(scraped_data)