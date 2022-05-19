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
        body = soup_article.find('div', {"id":"rtAnnouncements"})
        if body == None:
            n = n + 1
            continue
        else:
            corpaction = body.find_all('span', class_='hpEvent')
            corpactiondate = body.find_all('small', class_='date')
            corpac = []
            for p in range(len(corpaction)):
                corp = corpaction[p].get_text()
                date = corpactiondate[p].get_text()  
                insert_query =""" INSERT INTO itrader_corporateaction(security, action, date) VALUES (%s,%s,%s) """
                record_to_insert =(securities[n],corp,date)
                print(securities[n],corp,date)

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