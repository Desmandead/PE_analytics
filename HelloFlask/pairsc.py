import pandas as pd
from collections import Counter
import itertools

def pairs_compare(file_url,dir):
	df = pd.read_csv(file_url, sep=';')
	df = df.rename(columns={'Дата и время':'date','Номер':'order_id','Название':'sku','Количество':'sku_count','Общая сумма товара':'sku_sum'})
	df = df[['order_id','sku']]
	df.dropna()
	df.loc[df['sku'].str.contains(r'(?i)Пятнистый эублефар', case=False, na=False), 'sku'] = 'Эублефар'
	df.loc[df['sku'].str.contains(r'(?i)Бородатая агама', case=False, na=False), 'sku'] = 'Агама'
	df.loc[df['sku'].str.contains(r'(?i)Маисов', case=False, na=False), 'sku'] = 'Маисовый полоз'
	df.loc[df['sku'].str.contains(r'(?i)Реснитчатый геккон бананоед', case=False, na=False), 'sku'] = 'Реснитчатый геккон бананоед'
	df.loc[df['sku'].str.contains(r'(?i)Удав императорский', case=False, na=False), 'sku'] = 'Удав императорский'
	df.loc[df['sku'].str.contains(r'(?i)хамелеон ', case=False, na=False), 'sku'] = 'Хамелеон'
	df.loc[df['sku'].str.contains(r'(?i)паук-птицеед', case=False, na=False), 'sku'] = 'Паук-птицеед'
	df2 = df[['order_id','sku']]
	stat = df2.groupby('order_id').sku.agg(lambda x: list(itertools.combinations(x,2))).explode().str.join('--').value_counts()
	stat = stat.to_frame()
	stat = stat.reset_index()
	stat[['sku1','sku2']] = stat['index'].str.split('--', 1, expand=True)
	stat = stat.rename(columns={'sku':'count'})
	stat2 = stat[['sku1','sku2','count']]
	stat2.to_csv(dir + '/sku_pairs.csv', sep=';')
	fn = '/uploads/sku_pairs.csv'
	return fn