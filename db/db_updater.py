import yfinance as yf
import pandas as pd
from dotenv import load_dotenv
from yahoo_fin import stock_info as si
from datetime import datetime
from threading import Timer
import pymysql, calendar, os

import pdb


load_dotenv(dotenv_path='../.env')
database = os.getenv('DB')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')

class DBUpdater:
    def __init__(self):
        self.conn = pymysql.connect(host='localhost', user=user, password=password, db=database, charset='utf8')

        with self.conn.cursor() as cursor:
            create_company_infos = """
            CREATE TABLE IF NOT EXISTS company_infos (
                code VARCHAR(20),
                company VARCHAR(256),
                last_update DATE,
                PRIMARY KEY (code)
            );
            """
            cursor.execute(create_company_infos)
            create_daily_prices = """
            CREATE TABLE IF NOT EXISTS daily_prices (
                code VARCHAR(20),
                date DATE,
                open FLOAT,
                high FLOAT,
                low FLOAT,
                close FLOAT,
                diff FLOAT,
                volume FLOAT,
                PRIMARY KEY (code, date)
            );
            """
            cursor.execute(create_daily_prices)
        self.conn.commit()

        self.codes = dict()

    def __del__(self):
        self.conn.close()

    # TODO : 웹 스크래이핑으로 회사 정보 가져오기
    def nasdaq_tickers_and_company_names(self):
        nasdaq_list = pd.read_csv('../nasdaq_screener.csv')
        return nasdaq_list[['Symbol', 'Name']]

    def update_company_infos(self):
        sql = "SELECT * FROM company_infos"
        df = pd.read_sql(sql, self.conn)
        for idx in range(len(df)):
            self.codes[df['code'].values[idx]] = df['company'].values[idx]
        with self.conn.cursor() as cursor:
            sql = "SELECT max(last_update) FROM company_infos"
            cursor.execute(sql)
            rs = cursor.fetchone() # 최근 업데이트 날짜
            today = datetime.today().strftime('%Y-%m-%d')

            if True: #rs[0] == None or rs[0].strftime('%Y-%m-%d') < today:
                nasdaq_list = self.nasdaq_tickers_and_company_names()
                insert_failed_list = []
                for idx in range(len(nasdaq_list)):
                    try:
                        code = nasdaq_list['Symbol'].values[idx]
                        company = nasdaq_list['Name'].values[idx]
                        if len(company) > 256:
                            company = company[:256]
                        self.codes[code] = company
                        sql = """
                        REPLACE INTO company_infos (code, company, last_update)
                        VALUES (%s, %s, %s)
                        """
                        cursor.execute(sql, (code, company, today))
                        self.conn.commit()
                    except Exception as err:
                        insert_failed_list.append(code)
                        print(f"insert failed: {code}, {company}")
                print("** 회사 정보 업데이트 완료")
                print("** 회사 정보 업데이트 실패 리스트 : ", insert_failed_list)

    def get_price(self, ticker, start_date):
        end_date = datetime.today().strftime('%Y-%m-%d')
        df = yf.Ticker(ticker).history(period='1d', start=start_date, end=end_date)
        return df

    def replace_past_prices(self):
        with self.conn.cursor() as cursor:
            failed_list = []
            for ticker in self.codes.keys():
                sql = f"SELECT max(date) FROM daily_prices WHERE code = '{ticker}'"
                cursor.execute(sql)
                rs = cursor.fetchone()
                if rs[0] == None:
                    df = self.get_price(ticker, '2000-01-01')
                    for row in df.itertuples():
                        try:
                            sql = """
                            REPLACE INTO daily_prices (code, date, open, high, low, close, diff, volume)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                            """
                            cursor.execute(sql, (ticker, row.Index.strftime('%Y-%m-%d'), row.Open, row.High, row.Low, row.Close, row.Close - row.Open, row.Volume))
                            self.conn.commit()
                        except Exception as err:
                            failed_list.append(ticker)
                            print(f"** {ticker}의 일별 시세 업데이트 실패")
                    print(f"** {ticker}의 일별 시세 업데이트 완료")
            print("** 일별 시세 업데이트 실패 리스트 : ", failed_list)
            print("** 모든 종목의 일별 시세 업데이트 완료")

    def update_daily_prices(self):
        with self.conn.cursor() as cursor:
            for ticker in self.codes.keys():
                try:
                    df = yf.Ticker(ticker).history(period='1d').tail().iloc[0]
                    sql = """
                    REPLACE INTO daily_prices (code, date, open, high, low, close, diff, volume)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(sql, (ticker, datetime.today().strftime('%Y-%m-%d'), df.Open, df.High, df.Low, df.Close, df.Close - df.Open, df.Volume))
                    self.conn.commit()
                except Exception as err:
                    print(f"** {ticker}의 일별 시세 업데이트 실패")
        print("** 모든 종목의 일별 시세 업데이트 완료")

    def repeat_updating_daily_prices(self):
        self.update_daily_prices()

        tmnow = datetime.now()
        lastday = calendar.monthrange(tmnow.year, tmnow.month)[1]

        # TODO: 06:00 지정에도 문제없는지 확인 필요
        if tmnow.month == 12 and tmnow.day == lastday:
            tmnext = tmnow.replace(year=tmnow.year + 1, month=1, day=1, hour=6, minute=0, second=0)
        elif tmnow.day == lastday:
            tmnext = tmnow.replace(month=tmnow.month + 1, day=1, hour=6, minute=0, second=0)
        else:
            tmnext = tmnow.replace(day=tmnow.day + 1, hour=6, minute=0, second=0)
        tmdiff = tmnext - tmnow
        secs = tmdiff.seconds

        t = Timer(secs, self.update_daily_prices)
        print(f"** 다음 일별 시세 업데이트까지 {secs//60}분 {secs%60}초 남음")
        t.start()

if __name__ == "__main__":
    db_updater = DBUpdater()
    db_updater.update_company_infos()
    db_updater.replace_past_prices()
    # db_updater.repeat_updating_daily_prices()

