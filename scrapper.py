import json
import os
import requests
from bs4 import BeautifulSoup

def get_bbc_news_articles():
    url = 'https://www.bbc.com/news/world'
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to fetch news articles from BBC News. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract news articles
    articles_set = set()
    articles = []  # Initialize the list of articles

    for article in soup.find_all('div', class_='gs-c-promo'):
        title = article.find('h3', class_='gs-c-promo-heading__title').text.strip()

        # Check if the 'a' tag is found before accessing its attributes
        link_tag = article.find('a', class_='gs-c-promo-heading')
        if link_tag:
            link = url + link_tag.get('href', '').strip()
        else:
            link = ''

        # Check if the article with the same link already exists
        if link in articles_set:
            continue

        articles_set.add(link)

        # Check if the 'p' tag is found before accessing its text attribute
        description_tag = article.find('p', class_='gs-c-promo-summary')
        description = description_tag.text.strip() if description_tag else ''

        content = f"{title} {description}"  # Concatenate title and description for content
        articles.append({'title': title, 'link': link, 'description': description, 'content': content})

    # Get the directory of the current script
    script_directory = os.path.dirname(os.path.realpath(__file__))

    # Save unique articles to a JSON file in the same folder as the script
    json_file_path = os.path.join(script_directory, 'bbc_articles.json')
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(articles, json_file, ensure_ascii=False, indent=4)

    return articles

if __name__ == "__main__":
    get_bbc_news_articles()
