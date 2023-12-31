# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 14:14:16 2023

@author: THIS-LAPPY
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 10:50:37 2022

@author: THIS-LAPPY
"""


from flask import Flask,jsonify,render_template,redirect, url_for, session
from flask_cors import CORS, cross_origin
from flask import request
from collections.abc import Mapping
import requests,json,numpy as np,pandas as pd
from sqlalchemy import create_engine,text 

# from twilio.twiml.messaging_response import MessagingResponse
# import ee,os
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "ndvi12345-c712223647ab.json"
# ee.Initialize()
# os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
engine = create_engine('postgresql://root:oJmXhoHDzuGG3IZHnbnrEnRQR7QqLR5Q@dpg-cl6p55oicrhc73csvf10-a.oregon-postgres.render.com/afpldb')
conn = engine.connect()



app=Flask(__name__)
app.secret_key = 'rabbit1234567' 
CORS(app)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
@app.route('/home/')
def world():
    x='hello home'
    return x
    
# @app.route('/')
# def index():
#     return "<h1>Welcome to our server !!</h1>"


bmap=''
branchvila=''
empid=''
@app.route('/')
def index():
    # Check if the user is logged in before rendering the HTML template
    if 'username' in session:
       
            us=pd.read_sql(f"""select * from public.center_tag_pass where "Emp ID"='{empid}'""" ,conn).reset_index(drop=True)

            return render_template('center_tag.html',emp_id="Employee ID - "+us['Emp ID'][0],branch_name="Branch - "+us['Branch'][0],state="State - "+us['State'][0],district="District - "+us['District'][0],zone="Zone - "+us['Zone '][0],tehsil="Tehsil - "+us['Tehsil'][0])

        
    else:
        # Redirect to the login page if the user is not logged in
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get username and password from the login form
        username = request.form.get('username')
        password = request.form.get('password')
        global bmap
        bmap=request.form.get('mode')
        # Check credentials against the database
        if check_credentials(username, password):
            # Store the username in the session to mark the user as logged in
            session['username'] = username
            return redirect(url_for('index'))
        else:
            # Render the login page again with an error message
            return render_template('login.html', error='Invalid credentials')

    # Render the login page for GET requests
    return render_template('login.html')


@app.route('/logout')
def logout():
    # Clear the session to log the user out
    session.clear()
    # Redirect to the login page after logout
    return redirect(url_for('login'))

def check_credentials(username, password):
    # Implement your logic to check credentials against the database
    # Return True if the credentials are correct, False otherwise
    # This is a placeholder, replace it with your actual database logic
    us=pd.read_sql(f"""select * from public.center_tag_pass where "Emp ID"='{username}' and "password"='{password}'""" ,conn)
    if len(us)==1:
        global branchvila
        global empid
        branchvila= us['Branch'][0]
        empid=us['Emp ID'][0] 
        return username == us['Emp ID'][0] and password == us['password'][0] 
    else:
        return False


@app.route('/centertag/',methods=['POST'])
def centertag():
        empid = request.form.get('empid'),
        bid = request.form.get('bid'),
        zone = request.form.get('zone'),
        state = request.form.get('state'),
        district = request.form.get('district'),
        tehsil = request.form.get('tehsil'),
        vila = request.form.get('vila')
        lid = request.form.get('lid')
        cntrnm = request.form.get('cntrnm')
        cntrid = request.form.get('cntrid')
        lat = request.form.get('latitude')
        long = request.form.get('longitude')
        pin = request.form.get('pincode')
        phone = request.form.get('phone')
        dev=request.form.get('deviceInfo')   
        tim=request.form.get('timestamp')       
        response_data = {
           'Emp_id':str(empid).replace("Employee ID - ",''), 
           'Branch': str(bid).replace("Branch - ",''),
           'State': str(state).replace("State - ",''),
           'District':str(district).replace("District - ",''),
           'Tehsil':str(tehsil).replace("Tehsil - ",''),
           'zone': str(zone).replace("Zone - ",''),
           'Village':vila,
           'Loan_id':lid,
           'Center_name':cntrnm,
           'Center_id':cntrid,
           'Latitude':lat,
           'Longitude':long,
           'Pincode':pin,
           'Phone':phone,
           'Device_info':dev,
           'Timestamp':tim,
                              }
        rr=pd.DataFrame.from_records([response_data])
        rr.to_sql('center_tag',con=conn,if_exists='append',index=False)
        return response_data 


@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'no-store'
    return response


if __name__ == '__main__':
    app.run() 
