import pymysql
#import tensorflow as ts
import re
import numpy as np
pymysql_config = {
          'host':'127.0.0.1',
          'port':3306,
          'user':'root',
          'password':'m7227510',
          'db':'morningstar',
          'charset':'utf8mb4',
          'cursorclass':pymysql.cursors.DictCursor,
          }
db_fields_0=[
    ("morningstar_income_statement", "Revenue"),
    ("morningstar_income_statement", "Research and development"),
    ("morningstar_income_statement", "Operating income"),
    ("morningstar_income_statement", "Net income available to common shareholders"),
    ("morningstar_income_statement", "Earnings per shar"),
    ("morningstar_cash_flow", "Net income"),
    ("morningstar_cash_flow", "Stock based compensation"),
    ("morningstar_cash_flow",  "Accounts receivable"),
    ("morningstar_cash_flow",  "Net cash provided by operating activities"),
    ("morningstar_cash_flow",  "Cash Flows From Investing Activities"),
    ("morningstar_balance_sheet", "Assets"),
    ("morningstar_balance_sheet", "Current assets"),
    ("morningstar_balance_sheet", "Cash"),
    ("morningstar_balance_sheet", "Short-term investments"),
    ("morningstar_balance_sheet", "Inventories"),
    ("morningstar_balance_sheet", "Total current assets"),
    ("morningstar_balance_sheet", "Liabilities and stockholders' equity"),
    ("morningstar_balance_sheet", "Short-term debt"),
    ("morningstar_balance_sheet", "Accrued liabilities"),
    ("morningstar_balance_sheet", "Total liabilities"),
    ("morningstar_balance_sheet", "Retained earnings"),
    ("morningstar_balance_sheet", "Total stockholders' equity"),
    ("morningstar_balance_sheet", "Property, plant and equipment"),
    ("morningstar_balance_sheet", "Goodwill"),
    ("morningstar_balance_sheet", "Net property, plant and equipment")]
db_fields_1 =[
    ("morningstar_key_cash_flow_ratios", "operating_cash_flow_growth_percent_yoy"),
    ("morningstar_key_cash_flow_ratios", "free_cash_flow_growth_percent_yoy"),
    ("morningstar_key_cash_flow_ratios", "cap_ex_as_a_percent_of_sales"),
    ("morningstar_key_cash_flow_ratios", "free_cash_flow_per_sales_percent"),
    ("morningstar_key_cash_flow_ratios", "free_cash_flow_per_net_income")
]


class input_data():
    '''从数据库中取出指定股票、指定season的数据
    '''
    def __init__(self, conn, ticker="", season=""):
        self.ticker = ticker
        self.season = season
        self.conn = conn
        self.result = None #数据库中取出的原始数据。key是field的名字，value是值。None补0.
        self.vector_result=None
        self.matrix_result = None
    def get_data(self):
        pass

class input_data_db(input_data):
    def _get_data(self):
        self.result={}
        db_name = _get_db_name(self.ticker)
        year = self._convert_season_to_year()
        for table_and_field in db_fields_0:
            query =  "SELECT %s from %s" %(year ,table_and_field[0]) +\
                     " WHERE ticker = '%s'" %self.ticker +\
                     " and item='%s'" %table_and_field[1]
            try:
                result = _db_execute(query,self.conn, year)
                if(result is None):
                    self.result[table_and_field[1]]= 0.0
                else:
                    self.result[table_and_field[1]]= result
            except:
                self.result[table_and_field[1]]= 0.0
        for table_and_field in db_fields_1:
            query =  "SELECT %s from %s" %(table_and_field[1] ,table_and_field[0]) +\
                     " WHERE ticker = '%s'" %self.ticker +\
                     r" and date_format(period,'%Y')=" +\
                     "%s" %self.season[0:4]
            try:
                result = _db_execute(query,self.conn, table_and_field[1])
                if(result is None):
                    self.result[table_and_field[1]]= 0.0
                else:
                    self.result[table_and_field[1]]= result
            except:
                self.result[table_and_field[1]]= 0.0
        return self.result
    def _convert_season_to_year(self):
        return "year_"+self.season[:4]
    def get_data_origin(self):
        if(self.result is None):
            self._get_data()
        else:
            pass
        return self.result
    def get_data_vector(self):
        if(self.result is None):
            self._get_data()
        else:
            pass
        self.vector_result =[]
        for one_data in self.result:
            self.vector_result.append(float(self.result[one_data]))
        return self.vector_result
    def get_data_matrix(self):
        if(self.matrix_result is None):
            if(self.vector_result is None):
                vector_result = np.array(self.get_data_vector())
            else:
                vector_result = np.array(self.vector_result)
            mean = vector_result.mean()
            std = vector_result.std()
            for i in range(len(vector_result)):
                vector_result[i] = (vector_result[i]-mean)/std
            self.matrix_result= np.zeros((30,30))
            for ix in range(30):
                for iy in range(30):
                    self.matrix_result[ix,iy] = vector_result[ix]/vector_result[iy]
        else:
            pass
        return self.matrix_result

def _get_db_name(name):
    u"""Returns a new (cleaned) name that can be used in a MySQL database.



    :param name: Original name.

    :return Name that can be used in a MySQL database.

    """

    name = (name.lower()

            .replace(u'/', u' per ')

            .replace(u'&', u' and ')

            .replace(u'%', u' percent '))

    name = re.sub(r'[^a-z0-9]', u' ', name)

    name = re.sub(r'\s+', u' ', name).strip()

    return name.replace(u' ', u'_')

def _db_execute(query, conn, field):

    u"""Helper method for executing the given MySQL non-query.



    :param query: MySQL query to be executed.

    :param conn: MySQL connection.

    """

    cursor = conn.cursor()

    cursor.execute(query)
    result = cursor.fetchone()[field]
    cursor.close()
    return result

def matrixer():
    pass

def data_valide():
    #检验数据的有效性
    pass

def main():
    conn = pymysql.connect(**pymysql_config)
    with open("NYQ_tickers.csv","r") as f:
    #1. 指定ticker的名字
        ticker = f.readline()[:-1]
    #2. 指定年份和季度
        season = "201703"
    #3. 获取数据
        data = input_data_db(conn, ticker, season).get_data_matrix()
        # data = input_data_db(conn, ticker, season).get_data_vector()




if __name__ == '__main__':
    main()
