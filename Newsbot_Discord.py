import requests
from bs4 import BeautifulSoup
import json
import time

WEBHOOK_URL = 'ENTER HERE'
DARKREADING_URL = 'https://www.darkreading.com/ics-ot'
INTERVAL = 60 * 60  # Check every hour

def fetch_articles():
    response = requests.get(DARKREADING_URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    articles = soup.find_all('div', class_='entry-item')

    article_list = []
    for article in articles:
        title = article.find('h3').text.strip()
        link = article.find('a')['href']
        article_list.append({'title': title, 'link': link})
        print (article_list)

    return article_list

def send_to_discord(article):
    content = f"**{article['title']}**\n{article['link']}"
    data = {'content': content}
    requests.post(WEBHOOK_URL, json=data)
    print ("Sending News")

if __name__ == "__main__":
    last_articles = fetch_articles()

    while True:
        time.sleep(INTERVAL)
        print ("Checking....")
        new_articles = fetch_articles()

        for article in new_articles:
            if article not in last_articles:
                send_to_discord(article)

        last_articles = new_articles
