from flask import Flask, flash, request, redirect, url_for, render_template,send_file
import urllib.request
import os
from werkzeug.utils import secure_filename

import re

import parse
import pdfplumber
import pandas as pd
import numpy as np
from collections import namedtuple
from flask_cors import CORS
import matplotlib.pyplot as plt
import datetime
 
app = Flask(__name__)
CORS(app)
 
UPLOAD_FOLDER = 'static/uploads/'
 
#app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['csv','pdf'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     
 
statement = None
    
 
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return 'No file part'
        
    file = request.files['file']
    if file.filename == '':
        
        return 'No image selected for uploading'
    if file and allowed_file(file.filename):
        
        filess = file
        lines = []
        total_check = 0
        line_re = re.compile(r'(\d*\.\d*) (\d*\.\d*) (\d*\.\d*)')
        statement = pd.DataFrame( columns = ['Value Date', 'Transaction Date','Cheque Number','Transaction Remarks','Withdrawal Amount','Deposit Amount','Balance'])
        Value_Date=Transaction_Date=Cheque_Number=Transaction_Remarks=Withdrawal_Amount=Deposit_Amount=Balance=""
        with pdfplumber.open(file) as pdf:
            pages = pdf.pages
            #print(pages)
            i=0
            for page in pdf.pages:
                text = page.extract_text()
        
                for line in text.split('\n'):
                    # print(line)statement = pd.DataFrame( columns = ['Value Date', 'Transaction Date','Cheque Number','Transaction Remarks','Withdrawal Amount','Deposit Amount','Balance'])
                    if line_re.search(line):
                        i=i+1
                        li = line.split(" ")
                        comp=line_re.search(line)
                        Value_Date= li[0].replace(",","-"),li[1].replace(",","-"),li[3].split("/")[0],float(comp.group(1)), float(comp.group(2)),float(comp.group(3))    # li[0].replace(",","/")#pd.to_datetime(statement['Value Date'][2],format="%d/%m/%Y")
                        Transaction_Date=pd.to_datetime(li[1].replace(",","/"),format="%d/%m/%Y")
                        Cheque_Number=li[2]
                        Transaction_Remarks=li[3].split("/")[0]
                        
                        Withdrawal_Amount, Deposit_Amount,Balance = float(comp.group(1)), float(comp.group(2)),float(comp.group(3))
                        statement.loc[len(statement.index)]=[Value_Date,Transaction_Date,Cheque_Number,Transaction_Remarks,Withdrawal_Amount,Deposit_Amount,Balance]
                        #print(f"{i} vale={Value_Date} trs={Transaction_Date} che={Cheque_Number} dd={dd} one={vend_no} two={vend_name} three={three} ")
            
      
        
        return statement.to_json()
    else:
        
        return 'Allowed image types are - png, jpg, jpeg, gif'
 
@app.route("/graph", methods = ['GET','POST'])
def graph():
    
    fig = plt.figure(figsize = (10, 5))
    plt.bar(['min','max','avg'], [0, 31009, 7773.92482759], color ='maroon',width = 0.4)
 
    plt.xlabel("stats")
    plt.ylabel("Income")
    plt.title("Balance Analysis")
    plt.savefig("C:/trainproj/graph-img/figure.png", dpi=70)
    plt.show()
    return send_file("C:/trainproj/graph-img/figure.png",mimetype=("image/png"))
 
if __name__ == "__main__":
    app.run()