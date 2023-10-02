import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrape():
    URL = "https://www.phys.uniroma1.it/fisica/node/9879"
    # Establish a connection to the site
    page = requests.get(URL)
    # Obtain all the html from the site
    soup = BeautifulSoup(page.content, "html.parser")

    # Every single update is part of a list and every element of the list has the class "views_row"
    result = soup.find_all("li", class_="views-row")

    # Structure to store data easier in the pandas dataframe
    titles_data = []
    contents_data = []
    links_data = []
    for element in result:
        # Every title of the list is in a <span> tag situated inside the <strong> tag
        title = element.find("strong")
        titles_data.append(title.find("span").text.replace(" ", " ").strip())
        # --------------------------------------------------------------------------------------
        # The actual content is always written in a different style, this part covers most cases
        content = element.find("div", class_="field-content")
        if ".pdf" in content.text:
            # Don't remove this part since the dataframe needs all list to have the same number of elements
            contents_data.append("")
        else:
            contents_data.append(content.text.replace(" ", " ").strip())
        # --------------------------------------------------------------------------------------
        # Every link in the element is handles by this block
        links = element.find_all("a", href=True)
        sub_links = []  # There can be multiple links in a single news
        if type(links) is not None:
            if len(links) > 1:
                for link in links:
                    if "mailto" not in link['href']:  # Handles mails present in the href
                        sub_links.append(link['href'].replace(" ", " ").strip())
            elif len(links) == 1:
                if "mailto" not in links[0]['href']:  # Handles mails present in the href
                    sub_links.append(links[0]['href'].replace(" ", " ").strip())
        links_data.append(" ".join(sub_links))
        # --------------------------------------------------------------------------------------

    data = {"Titles": titles_data, "Contents": contents_data, "Links": links_data}
    df = pd.DataFrame(data)

    return df


def save_excel(df, name):
    df.to_excel(name)
