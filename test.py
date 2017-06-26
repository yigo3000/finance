import good_morning as gm
import pymysql.cursors

pymysql_config = {
          'host':'127.0.0.1',
          'port':3306,
          'user':'root',
          'password':'m7227510',
          'db':'morningstar',
          'charset':'utf8mb4',
          'cursorclass':pymysql.cursors.DictCursor,
          }
# Connect to the database
connection = pymysql.connect(**pymysql_config)

#kr = gm.KeyRatiosDownloader()
#kr_frames = kr.download('AAPL',connection)
kr = gm.FinancialsDownloader()
kr_frames = kr.download('AAPL',connection)
print(kr_frames)
'''for krf in kr_frames:
    print(krf.index.name)
    for idvl in krf.index.values:
        print(idvl)

'''