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

    # cursor
    cur = con.cursor()
    securities = cur.execute('''select security from itrader_stockdata''')
    securities = [sec[0] for sec in cur.fetchall()]

    print(securities)


    for n in range(len(securities)):
        # Reading the content
        link =('https://live.mystocks.co.ke/stock=' + securities[n])
        print(link)
        article = requests.get(link)
        article_content = article.content
        soup_article = BeautifulSoup(article_content, 'html.parser')
        body = soup_article.find(class_='stockProfile')
        x = body.find_all('p')
        list_paragraphs = []
        for p in range(len(x)):
            paragraph = x[p].get_text()
            list_paragraphs.append(paragraph)
            insert_query =""" INSERT INTO itrader_companyprofile(security, profile) VALUES (%s,%s) """
        final_article = " ".join(list_paragraphs)
        record_to_insert =(securities[n],final_article)

        # execute query
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