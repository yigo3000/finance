# -*- coding: UTF-8 -*-
'''
从morning star获取财务数据
'''

import good_morning as gm
import pymysql.cursors
import pickle
import logging
from tkinter import *
def load_from_ms(connection,exchange,GUI=False,text_handle=None):
    # connection: pymysql.connect(**pymysql_config),用于连接数据库
    # exchange： str类型，交易所的缩写。例如：
    # 缩写          全名                     爬到公司数量
    # NYQ: New York Stock Exchange        3393 靠谱
    # ASE:  全美证券交易所       839 靠谱
    # BTS:  比特币      1
    # NCM:   NasdaqCM 纳斯达克资本市场     861
    # NGM:   纳斯达克全球市场     487
    # NMS：   纳斯达克全球精选      1775   完美世界在这里
    # OBB：  美国场外柜台交易系统      223
    # PCX:        36
    # PNK:   ?有多伦多股市     14405
    #GUI: 是否使用GUI调用该函数。当GUI=True时，应该传递一个text_handle，用来输出信息。
    index = 0
    try:
        with open(exchange+'index.pkl',"rb") as pkf:
            index = pickle.load(pkf)
    except:
        with open(exchange+'index.pkl',"wb") as f:
            pickle.dump(0,f)
    with open(exchange+'_tickers.csv','r') as f:
        try:
            tickers = f.readlines()
            while(index < len(tickers)):
                try:
                    ticker = tickers[index][:-1]
                    #connection = pymysql.connect(**pymysql_config)  # Connect to the database
                    kr = gm.KeyRatiosDownloader()
                    kr_frames = kr.download(ticker,connection)
                    Fi = gm.FinancialsDownloader()
                    Fi_frames = Fi.download(ticker,connection)
                    index += 1
                    message = "%d: " %index + ticker+" is done."
                    print(message)
                    if(GUI):
                        text_handle.insert(END,message+'\n')
                except Exception as ex:
                    index += 1
                    message = "%d: " %index + "Got exception, but we'll go on."
                    print(message)
                    if(GUI):
                        text_handle.insert(END,message+'\n')
                    #logger.debug(ex)
        except Exception as ex:
            message = "A exception occurred while downloading. Suspending downloader to disk"
            print(message)
            if(GUI):
                text_handle.insert(END,message+'\n')
            with open('index.pkl',"wb") as pkf:
                pickle.dump(index,pkf)
            message = "Successfully saved download state"
            print(message)
            if(GUI):
                text_handle.insert(END,message+'\n')
            message = "Try removing {type}.pickle file if this error persists"
            print(message)
            if(GUI):
                text_handle.insert(END,message+'\n')
        except KeyboardInterrupt as ex:
            with open('index.pkl',"wb") as pkf:
                pickle.dump(index,pkf)
def main():
    logger = logging.getLogger("mylog")
    formatter = logging.Formatter('%(name)-12s %(asctime)s %(levelname)-8s %(message)s', '%a, %d %b %Y %H:%M:%S',)
    file_handler = logging.FileHandler("load_from_ms.txt",encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)

    pymysql_config = {
              'host':'127.0.0.1',
              'port':3306,
              'user':'root',
              'password':'m7227510',
              'db':'morningstar',
              'charset':'utf8mb4',
              'cursorclass':pymysql.cursors.DictCursor,
              }
    index = 0
    with open('load_from_ms.pkl',"wb") as f:
        pickle.dump(0,f)

    with open('load_from_ms.pkl',"rb") as pkf, open('NYQ_not_download.csv','r') as f:
        try:
            index = pickle.load(pkf)
        except:
                pass
        try:
            tickers = f.readlines()
            while(index < len(tickers)):
                try:
                    ticker = tickers[index][:-1]
                    connection = pymysql.connect(**pymysql_config)  # Connect to the database
                    kr = gm.KeyRatiosDownloader()
                    kr_frames = kr.download(ticker,connection)
                    Fi = gm.FinancialsDownloader()
                    Fi_frames = Fi.download(ticker,connection)
                    index += 1
                    print("%d: " %index + ticker+" is done(success or failed).")
                except Exception as ex:
                    print("%d: " %index + "Got exception, but we'll go on.")
                    logger.debug(ex)
        except Exception as ex:
            print("A exception occurred while downloading. Suspending downloader to disk")
            with open('load_from_ms.pkl',"wb") as pkf:
                pickle.dump(index,pkf)
            print("Successfully saved download state")
            print("Try removing {type}.pickle file if this error persists")
        except KeyboardInterrupt as ex:
            with open('load_from_ms.pkl',"wb") as pkf:
                pickle.dump(index,pkf)




if __name__ == '__main__':
    main()