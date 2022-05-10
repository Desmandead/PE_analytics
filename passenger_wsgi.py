# -*- coding: utf-8 -*-
import sys, os
sys.path.append('/home/s/stepfi2k/nd.planetexotic.ru/HelloFlask/') # указываем директорию с проектом
sys.path.append('/home/s/stepfi2k/.local/lib/python3.6/site-packages/') # указываем директорию с библиотеками, куда поставили Flask
from HelloFlask import app as application # когда Flask стартует, он ищет application. Если не указать 'as application', сайт не заработает
from werkzeug.debug import DebuggedApplication # Опционально: подключение модуля отладки
application.wsgi_app = DebuggedApplication(application.wsgi_app, True) # Опционально: включение модуля отадки
application.debug = True  # Опционально: True/False устанавливается по необходимости в отладке