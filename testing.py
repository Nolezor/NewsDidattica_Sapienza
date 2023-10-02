import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrape():
    URL = "https://www.phys.uniroma1.it/fisica/node/9879"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    result = soup.find_all("li", class_="views-row")

    titles_data = []
    contents_data = []
    links_data = []
    for element in result:
        title = element.find("strong")
        titles_data.append(title.find("span").text.replace(" ", " ").strip())
        content = element.find("div", class_="field-content")
        if ".pdf" in content.text:
            contents_data.append("")
        else:
            contents_data.append(content.text.replace(" ", " ").strip())
        links = element.find_all("a", href=True)
        sub_links = []
        if type(links) is not None:
            if len(links) > 1:
                for link in links:
                    if "mailto" not in link['href']:
                        sub_links.append(link['href'].replace(" ", " ").strip())
            elif len(links) == 1:
                if "mailto" not in links[0]['href']:
                    sub_links.append(links[0]['href'].replace(" ", " ").strip())
        links_data.append(" ".join(sub_links))

    data = {"Titles": titles_data, "Contents": contents_data, "Links": links_data}

    df = pd.DataFrame(data)
    return df


def save_excel(df, name):
    df.to_excel(name)


if __name__ == '__main__':
    save_excel(scrape(), "tests.xlsx")
