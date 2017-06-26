# -*- coding: UTF-8 -*-
'''
从morning star获取财务数据
'''

import good_morning as gm
import pymysql.cursors
import pickle
import logging
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
