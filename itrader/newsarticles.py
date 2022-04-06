# import numpy as np
import requests
from bs4 import BeautifulSoup
import psycopg2

try:
    #connect to the db
    con = psycopg2.connect(
        host = 'localhost',
        database = 'trading',
        user = 'postgres',
        password = 'postgres',
        port = 5432
    )

    #cursor
    cur = con.cursor()
        
    #Get HTML content
    r1 = requests.get("https://www.businessdailyafrica.com/bd/markets")
    coverpage = r1.content

    #Create soup
    soup1 = BeautifulSoup(coverpage, 'html.parser')
    coverpage_news = soup1.find_all('article', class_='article article-list-regular')
    coverpage_news[4].get_text()


    number_of_articles = 10
    news_contents = []
    list_links = []
    list_titles = []

    for n in range(number_of_articles):
        # Get link of the article
        link = coverpage_news[n].find('a')['href']
        list_links.append(link)

        #Get the Title
        title = coverpage_news[n].find('a').get_text()
        list_titles.append(title)

        #Reading the content
        link =('https://www.businessdailyafrica.com'+link)
        article = requests.get(link)
        article_content = article.content
        soup_article = BeautifulSoup(article_content, 'html.parser')
        date = soup_article.find('small', class_='byline').get_text()
        body = soup_article.find_all('article', class_='article-story page-box')
        x = body[0].find_all('p')
        list_paragraphs = []
        for p in range(len(x)):
            paragraph = x[p].get_text()
            list_paragraphs.append(paragraph)
            insert_query =""" INSERT INTO itrader_news(title, link, content, date) VALUES (%s,%s,%s,%s) """
        final_article = " ".join(list_paragraphs)
        record_to_insert =(title,link,final_article,date)

        news_contents.append(final_article)

        #execute query
        cur.execute(insert_query, record_to_insert)
        con.commit()
        count = cur.rowcount
        print(count, "Record inserted successfully into news table")
    
except (Exception, psycopg2.Error) as error:
    print("Failed to insert record into news table", error)
finally:
    # closing database connection.
    if con:
        cur.close()
        con.close()
        print("PostgreSQL connection is closed")