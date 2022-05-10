from flask import Flask, render_template, send_file, request,redirect,url_for
app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'

import os
from werkzeug.utils import secure_filename
from flask import send_from_directory
from forms import LoginForm
import numpy as np
import pandas as pd

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 

@app.route('/')
def index():
	return render_template("index.html")
	
@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)

@app.route('/upload')
def upload():
	return render_template("upload.html")    

@app.route('/url', methods=['GET', 'POST'])
def some_sum():
    q = request.form.get('q')
    #q ='eaouaeou'
    return render_template('index.html', peremen=q)
    
@app.route('/upload2',methods = ['GET','POST'])
def upload_file():
    if request.method =='POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            basedir = os.path.abspath(os.path.dirname(__file__))
            file.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))
            #file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            from ltvan import ltv
            filename=basedir+'/'+ app.config['UPLOAD_FOLDER']+'/'+filename
            ltvr = ltv(filename)
    else:
     	basedir='Файл не загружен'
     	ltvr=''
    return render_template('upload2.html', filename=ltvr)
    
@app.route('/pairs',methods = ['GET','POST'])
def pair_func():
	if request.method =='POST':
		file = request.files['file']
		if file:
		    filename = secure_filename(file.filename)
		    basedir = os.path.abspath(os.path.dirname(__file__))
		    file.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))
		    #file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
		    from pairsc import pairs_compare
		    dir = basedir+'/'+ app.config['UPLOAD_FOLDER']
		    filename=basedir+'/'+ app.config['UPLOAD_FOLDER']+'/'+filename
		    linktofile = pairs_compare(filename,dir)
	else:
	 	basedir='Файл не загружен'
	 	linktofile=''
	return render_template('pairs.html', linka=linktofile)
	
@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'])+'/'+filename
    #path = "/"+filename
    return send_file(uploads, as_attachment=True)
    #return send_from_directory(directory=uploads, filename=filename)	

@app.route('/speed',methods = ['GET','POST'])
def speed_sku():
    if request.method =='POST':
        from speed import real_speed 
        basedir = os.path.abspath(os.path.dirname(__file__))
        dir = basedir+'/'+ app.config['UPLOAD_FOLDER']
        linktofile = real_speed(dir)
        linkt='Скачать файл'
    else:
    	linktofile ='#'
    	linkt=''
    return render_template('speed.html',  linka=linktofile, linktext=linkt)
    #return render_template('speed.html',  tables=[ltvr.to_html(classes='data')], titles=ltvr.columns.values)
    

if __name__ == '__main__':
    app.run()