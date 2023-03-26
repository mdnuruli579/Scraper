from django.shortcuts import HttpResponse
import requests
import csv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import sqlite3
import datetime

def index(request):
    
    url = "https://www.theverge.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    articles = soup.find_all('article')
    filename = datetime.datetime.now().strftime("%d%m%Y") + "_verge.db"
    filname = datetime.datetime.now().strftime("%d%m%Y") + "_verge.csv"
    conn = sqlite3.connect(filename)
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    session.get(url)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE articles (id INTEGER PRIMARY KEY,URL TEXT,headline TEXT,author TEXT,date TEXT)''')
    with open(filname, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'URL', 'headline', 'author', 'date'])
        for i, article in enumerate(articles):
            headline = article.find('h2').text.strip()
            link = article.find('a')['href']
            byline = article.find('div', class_='c-byline')
            author = byline.find('a', class_='c-byline__author-name').text.strip()
            date = byline.find('time')['datetime']
            cursor.execute("INSERT INTO articles (id, URL, headline, author, date) VALUES (?, ?, ?, ?, ?)",(i+1, link, headline, author, date))
            writer.writerow([i+1, link, headline, author, date])
            # print(f"Article {i+1}")
            # print("Headline:", headline)
            # print("Link:", link)
            # print("Author:", author)
            # print("Date:", date)
            # print()
    conn.commit()
    conn.close()
    print(f"SQLite database '{filename}' has been created successfully!")
    return HttpResponse("<h3>Successfully</h3>")
