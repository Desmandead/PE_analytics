import pandas as pd

def ltv(file_url):
	df = pd.read_csv(file_url, sep=';')
	df = df.astype({'cid':'str'})
	df = df.rename(columns={'Покупатель':'name_user','Контактный телефон':'phone_number','E-mail':'email','Сумма':'order_summ','Дата и время':'order_date','Статус заказа':'status','Тип контрагента':'type_client'})
	opt = df.query('type_client != "Физическое лицо"')
	online = df.query('type_client == "Физическое лицо" and status == "Выполнен онлайн"')
	zal =  df.query('type_client == "Физическое лицо" and status == "Выполнен зал"')
	zo = df.query('type_client == "Физическое лицо"')
	aov_opt = opt.order_summ.mean()
	aov_zal = zal.order_summ.mean()
	aov_online = online.order_summ.mean()
	aov_zo = zo.order_summ.mean()
	ltv_opt = opt.groupby('phone_number', as_index=False) \
	    .agg({'order_date':'count'}) \
	    .rename(columns={'order_date':'count_orders'})
	    #.query('count_orders >= 2')
	ltv_zal = zal.groupby('phone_number', as_index=False) \
	    .agg({'order_date':'count'}) \
	    .rename(columns={'order_date':'count_orders'})
	ltv_online = online.groupby('phone_number', as_index=False) \
	    .agg({'order_date':'count'}) \
	    .rename(columns={'order_date':'count_orders'})
	ltv_zo = zo.groupby('phone_number', as_index=False) \
	    .agg({'order_date':'count'}) \
	    .rename(columns={'order_date':'count_orders'})
	atv_zal = ltv_zal.count_orders.mean()
	atv_opt = ltv_opt.count_orders.mean()
	atv_online = ltv_online.count_orders.mean()
	atv_zo = ltv_zo.count_orders.mean()
	ltvzal = aov_zal*atv_zal
	#print('Зал:',round(ltvzal),round(aov_zal),atv_zal)
	ltvopt = aov_opt*atv_opt
	#print('Опт:',round(ltvopt),round(aov_opt),atv_opt)
	ltvonline = aov_online*atv_online
	#print('Онлайн:',round(ltvonline),round(aov_online),atv_online)
	ltvzo = aov_zo*atv_zo
	#print('Зал+Онлайн:',round(ltvzo),round(aov_zo),atv_zo)
	res = dict()
	res['zalatv'] = atv_zal
	res['zalaov'] = round(aov_zal)
	res['zalltv'] = round(ltvzal)
	
	res['onlineatv'] = atv_online
	res['onlineaov'] = round(aov_online)
	res['onlineltv'] = round(ltvonline)
	
	res['optatv'] = atv_opt
	res['optaov'] = round(aov_opt)
	res['optltv'] = round(ltvopt)
	
	res['zoatv'] = atv_zo
	res['zoaov'] = round(aov_zo)
	res['zoltv'] = round(ltvzo)
	return res
