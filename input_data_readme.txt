使用方法：
pip install -r requeriments.txt
input_data中把pymysql_config修改为自己的数据库配置。
指定股票名、年份和季度，然后：
data = input_data_NYQ(conn, ticker, season).get_data_matrix()
注：当前的30个数都是每年发布一次，所以现在season="201603"和season="201609"是一样的。

调用input_data的方法:
参考input_data中的main()中的方法。

测试input_data的方法：
拷贝NYQ_tickers.csv文件到路径下，直接python input_daya.py即可。

tips:
1. 数据库中的field，不同的公司也不一样。
例如:AAPL有这一项("morningstar_income_statement", "Research and development"),
而好多公司（如tco）没有。
没有的数据全部补0.