import pandas as pd 
import pymysql 

if __name__ =='__main__':
    db_host='localhost'
    db_user='sec_user'
    db_pass='password'
    db_name='securities_master'
    con=pymysql.connect(db_host,db_user,db_pass,db_name)
    sql = ' SELECT dp.price_date, dp.adj_close_price FROM symbol AS sym INNER JOIN daily_price AS dp ON dp.symbol_id =sym.id WHERE sym.ticker =\'GOOG\' ORDER BY dp.price_date ASC;'
    goog = pd.read_sql_query(sql,con=con,index_col='price_date')
    print(goog.tail())