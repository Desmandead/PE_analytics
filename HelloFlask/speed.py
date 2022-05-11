import pandas as pd
import requests
from sqlalchemy import create_engine
import json
from datetime import date
from dateutil.relativedelta import relativedelta
import time



def real_speed(dir):

#	Get how long sku was it in	stock
	six_months = date.today() + relativedelta(months=-6)
	cnx = create_engine('mysql://stepfi2k_speed:Speed123@localhost/stepfi2k_speed?charset=utf8').connect()
	sql = 'select name, COUNT(date) from real_speed WHERE quantity>0 AND date>"'+str(six_months)+'" GROUP BY name'
	df_stock = pd.read_sql(sql, cnx)
	
	with cnx.connect() as connection:
		result = connection.execute("select MIN(date) from real_speed")
		for row in result:
			#print(row['MIN(date)'], file=sys.stderr)
			mindate = row['MIN(date)']
	
# 	Get sell quantity and calculation selling speed for each sku
	response = get('https://online.moysklad.ru/api/remap/1.2/report/profit/byvariant?momentFrom='+str(six_months), auth=('finance@emelyanovroman', 'financePE2021'))
	js = (response.json())
	df = pd.DataFrame.from_dict(js['rows'])
	name = pd.json_normalize(df['assortment'])
	result = name['name']
	result = result.to_frame()
	sell = df['sellQuantity']
	sell = sell.to_frame()
	result = result.join(sell)
	
	main = df_stock.merge(result, how='left', on='name')
	main['real_speed'] = main['sellQuantity']/main['COUNT(date)']
	
	
# 	-------------------------------------------------
# 	response = get('https://planetexotic3.retailcrm.ru/api/v5/store/products?filter[active]=1&filter[priceType]=opt&filter[minPrice]=1&apiKey=ujYoZWfqjwTmGkYN9igibnv70jxuEzHq&limit=100&page=1')
# 	js = (response.json())
# 	df = pd.json_normalize(js['products'],['offers'], errors='ignore')
# 	
# 	page=2
# 	while page<=20:
# 	    response = get('https://planetexotic3.retailcrm.ru/api/v5/store/products?filter[active]=1&apiKey=ujYoZWfqjwTmGkYN9igibnv70jxuEzHq&limit=100&page='+str(page))
# 	    js = (response.json())
# 	    df2 = pd.json_normalize(js['products'],['offers'], errors='ignore')
# 	    df = pd.concat([df,df2] ,ignore_index=True)
# 	    if page % 7 == 0:
# 	        time.sleep(1)
# 	    page +=1
# 	
# # 	df2 = df.explode('prices').dropna(subset=['prices']).reset_index(drop=True)
# 	
# 	df3 = df[['xmlId','prices']]
# 	
# 	df5 = pd.concat(
# 	    [df3, df.explode("prices")["prices"].apply(pd.Series)], axis=1
# 	).drop(columns="prices")
# 	
# 	df6 = df5.query('priceType == "opt"')
# 	df6['xmlId'] = df6['xmlId'].str.replace(r'(.*#)', '', regex=True)
# 	df6 = df6.rename(columns={'xmlId':'externalCode'})




#	Get matching xmlId with price type from CRM
#	To speed up the script, it was decided to load the price type to the external code via csv
	df6 = pd.read_csv(dir + '/opt_price_externalCode.csv')
# -----------------------------------------------


#	Get moysklad token
	response = post('https://online.moysklad.ru/api/remap/1.2/security/token', auth=('finance@emelyanovroman', 'financePE2021'))
	js = (response.json())
	access_token = js['access_token']
	class BearerAuth(requests.auth.AuthBase):
	    def __init__(self, token):
	        self.token = token
	    def __call__(self, r):
	        r.headers["authorization"] = "Bearer " + self.token
	        return r
	        
#	Get quantity sku and merge all dataframe
	offset=0
	response = get('https://online.moysklad.ru/api/remap/1.2/entity/assortment?offset='+str(offset) +'&limit=1000', auth=BearerAuth(access_token))
	js = (response.json())
	dfm = pd.DataFrame.from_dict(js['rows'])
	offset=1000
	while offset<=5000:
	    response = get('https://online.moysklad.ru/api/remap/1.2/entity/assortment?offset='+str(offset) +'&limit=1000', auth=BearerAuth(access_token))
	    js = (response.json())
	    dfm = dfm.append(pd.DataFrame.from_dict(js['rows']))
	    offset +=1000
	quant = dfm[['name','quantity','externalCode']]
	quant = quant.merge(df6, how='left', on='externalCode')
	main = main.merge(quant, how='left', on='name')
	main['balance_by_day'] = main['quantity']/main['real_speed']
	
	main.to_csv(dir + '/real_speed.csv', sep=';')
	rs = '/uploads/real_speed.csv'
	return(rs)