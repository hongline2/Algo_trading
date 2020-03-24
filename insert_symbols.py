from __future__ import print_function
import datetime
from math import ceil
import bs4
import pymysql.cursors
import pymysql
import requests
def obtain_parse_wiki_snp500():
    """
    Download and parse the Wikipedia list of S&P500
    constituents using requests and BeautifulSoup.
    Returns a list of tuples for to add to MySQL.
    """

    now = datetime.datetime.utcnow()

    response = requests.get(    "http://en.wikipedia.org/wiki/List_of_S%26P_500_companies"    )
    soup = bs4.BeautifulSoup(response.text)

    symbolslist = soup.select('table')[0].select('tr')[1:]

    symbols = []
    for i, symbol in enumerate(symbolslist):
        tds = symbol.select('td')
        symbols.append(
        (
        tds[0].select('a')[0].text, # Ticker
        'stock',
        tds[1].select('a')[0].text, # Name
        
        tds[3].text, # Sector
        'USD', now, now
        )
        )
    return symbols
def insert_snp500_symbols(symbols):
    """
    Insert the S&P500 symbols into the MySQL database.
    """

    db_host = 'localhost'
    db_user = 'sec_user'
    db_pass = 'password'
    db_name = 'securities_master'
    connection = pymysql.connect(host=db_host, user=db_user, passwd=db_pass, db=db_name)
# Create the insert strings
    column_str = "ticker, instrument, name, sector,currency, created_date, last_updated_date"
    insert_str = ("%s, " * 7)[:-2]
    final_str = "INSERT INTO symbol (%s) VALUES (%s)" % (column_str, insert_str)
# Using the MySQL connection, carry out
# an INSERT INTO for every symbol
    with connection.cursor() as cursor:
        # Create a new record
        cursor.executemany(final_str,symbols)

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()
    connection.close()

if __name__ == "__main__":
    symbols = obtain_parse_wiki_snp500()
    insert_snp500_symbols(symbols)
    print("%s symbols were successfully added." % len(symbols))