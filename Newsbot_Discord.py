import feedparser
import requests
import time
from datetime import datetime, date
from email.utils import parsedate

WEBHOOK_URL = 'https://discordapp.com/api/webhooks/xxxxx'
INTERVAL = 10 * 60  # Check every 10 minutes

RSS_FEEDS = [
    'https://www.darkreading.com/rss.xml',
    'https://feeds.feedburner.com/TheHackersNews',
    'https://threatpost.com/feed/',
    'https://www.securityweek.com/rss',
    'https://www.scmagazine.com/home/security-news/feed/',
    'https://www.infosecurity-magazine.com/rss/news/',
    'https://www.zdnet.com/topic/security/rss.xml',
    'https://www.bleepingcomputer.com/feed/',
    'https://www.cyberscoop.com/feed/',
    'https://securityintelligence.com/feed/',
    'https://www.wired.com/feed/category/security/latest/rss',
]


KEYWORDS = ['Industrial', 'Critical', 'ICS', 'SCADA', 'PLC', 'Distributed Control System', 'HMI', 'Supervisory Control and Data Acquisition', 'Programmable Logic Controller', 'Process Control', 'Process Automation', 'Cybersecurity', 'Network Security', 'Risk Assessment', 'Intrusion Detection', 'malware', 'Intrusion Prevention', 'Security Policies']



def fetch_articles():
    article_list = []
    today = date.today()
    print("Today I found these on", today)

    for rss_feed in RSS_FEEDS:
        feed = feedparser.parse(rss_feed)

        for entry in feed.entries:
            published_date = parsedate(entry.published)

            if published_date is None:
                continue

            published_date = datetime.fromtimestamp(time.mktime(published_date)).date()

            # Check if the article was published on the same day
            if published_date == today:
                title = entry.title
                link = entry.link
                summary = entry.summary

                # Check if any of the keywords are present in the article title or summary
                if any(keyword in title or keyword in summary for keyword in KEYWORDS):
                    article_list.append({'title': title, 'link': link})
                    print("NEWS PUSH", title)

    return article_list


def send_to_discord(article):
    content = f"**{article['title']}**\n{article['link']}"
    data = {'content': content}
    requests.post(WEBHOOK_URL, json=data)
    print("Did I do good ")


if __name__ == "__main__":
    while True:
        articles = fetch_articles()

        for article in articles:
            send_to_discord(article)

        time.sleep(INTERVAL)
