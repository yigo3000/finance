ʹ�÷�����
pip install -r requeriments.txt
input_data�а�pymysql_config�޸�Ϊ�Լ������ݿ����á�
ָ����Ʊ������ݺͼ��ȣ�Ȼ��
data = input_data_NYQ(conn, ticker, season).get_data_matrix()
ע����ǰ��30��������ÿ�귢��һ�Σ���������season="201603"��season="201609"��һ���ġ�

����input_data�ķ���:
�ο�input_data�е�main()�еķ�����

����input_data�ķ�����
����NYQ_tickers.csv�ļ���·���£�ֱ��python input_daya.py���ɡ�

tips:
1. ���ݿ��е�field����ͬ�Ĺ�˾Ҳ��һ����
����:AAPL����һ��("morningstar_income_statement", "Research and development"),
���ö๫˾����tco��û�С�
û�е�����ȫ����0.