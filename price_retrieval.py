import datetime
import warnings
import pymysql
import requests
import yfinance as yf
import numpy as np 
# Obtain a database connection to the MySQL instance

pymysql.converters.encoders[np.float64] = pymysql.converters.escape_float
pymysql.converters.conversions = pymysql.converters.encoders.copy()
pymysql.converters.conversions.update(pymysql.converters.decoders)

db_host = 'localhost'
db_user = 'sec_user'
db_pass = 'password'
db_name = 'securities_master'
con = pymysql.connect(host=db_host, user=db_user, passwd=db_pass, db=db_name)
def obtain_list_of_db_tickers():
    with con.cursor() as cursor:
        cursor.execute('SELECT id, ticker FROM symbol')
        data=cursor.fetchall()
    con.commit()
    con.close()
    return [(d[0], d[1]) for d in data]

def get_daily_historic_data_yahoo(ticker, start_date='2000-01-01',end_date=datetime.date.today().timetuple()[0:3]):
    yahoo_cur=yf.Ticker(ticker)
    data=yahoo_cur.history(start_date=start_date, end_date=end_date,auto_adjust=False)
    return data

def insert_daily_data_into_db(data_vendor_id,symbol_id,daily_data):
    now=datetime.datetime.utcnow()
    column_str='data_vendor_id, symbol_id, price_date, created_date, last_updated_date, open_price, high_price, low_price, close_price, volume, adj_close_price'
    insert_str= ('%s, '*11)[:-2]
    final_str='INSERT INTO daily_price (%s) VALUES (%s)' %(column_str,insert_str)
    
    data=[(data_vendor_id,symbol_id,datetime.datetime.strptime(str(d[0])[:10],'%Y-%m-%d'),now,now,float(d[1][0]),float(d[1][1]),float(d[1][2]),float(d[1][3]),float(d[1][5]),int(d[1][4])) for d in daily_data.iterrows()]


    connection = pymysql.connect(host=db_host, user=db_user, passwd=db_pass, db=db_name)
    with connection.cursor() as cursor:
        # Create a new record
        cursor.executemany(final_str,data)

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()
    connection.close()

if __name__ == '__main__':
    warnings.filterwarnings('ignore')
    tickers=obtain_list_of_db_tickers()
    lentickers=len(tickers)
    for i,t in enumerate(tickers):
        print('adding data for %s: %s out of %s'%(t[1],i+1,lentickers))
        yf_data=get_daily_historic_data_yahoo(t[1])
        insert_daily_data_into_db(1,t[0],yf_data)
    print('successfully added yahoo finance data')
    