# import numpy as np
import requests
from bs4 import BeautifulSoup
import psycopg2
from nltk.sentiment.vader import SentimentIntensityAnalyzer

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
    r1 = requests.get("https://www.businessdailyafrica.com/bd/corporate")
    r1.encoding = 'utf-8'
    coverpage = r1.content

    #Create soup
    soup1 = BeautifulSoup(coverpage, 'html.parser')
    coverpage_news = soup1.find_all('article', class_='article article-list-regular')
    coverpage_news[4].get_text()


    number_of_articles = 30


    for n in range(number_of_articles):
        # Get link of the article
        link = coverpage_news[n].find('a')['href']

        #Get the Title
        title = coverpage_news[n].find('a').get_text()

        #Reading the content
        link =('https://www.businessdailyafrica.com'+link)
        article = requests.get(link)
        article_content = article.content
        soup_article = BeautifulSoup(article_content, 'html.parser')

        #Get the Date
        date = soup_article.find('small', class_='byline').get_text()

        #Get text
        body = soup_article.find_all('article', class_='article-story page-box')
        x = body[0].find_all('p')
        list_paragraphs = []
        for p in range(len(x)):
            paragraph = x[p].get_text()
            list_paragraphs.append(paragraph)
        final_article = " ".join(list_paragraphs)

       
        # analyser = SentimentIntensityAnalyzer()

        # create function to compute sentiment score
        def sentiment_score_calc(content):
            return analyser.polarity_scores(content)["compound"]

        #create new object  #Create a VADER sentiment analyzer
        analyser = SentimentIntensityAnalyzer()

        #Apply the sentiment_score_calc function
        sentiment_score = sentiment_score_calc(final_article)              
        insert_query =""" INSERT INTO itrader_news(title, link, content, date, sentimentscore) VALUES (%s,%s,%s,%s,%s) """

        record_to_insert =(title,link,final_article,date,sentiment_score)

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