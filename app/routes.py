import json
from json2html import *
import calendar
from datetime import datetime
from sqlalchemy.sql import text
from flask import request, jsonify, make_response, render_template
import json
import re
import random
import string
import array
import requests
import json
from app import app, db, logger, Config
from app.models import Deploy
from app.schema import deployment_schema, deployments_schema
from flask import send_from_directory, render_template
from collections import OrderedDict
from datetime import datetime, timedelta, date






@app.route("/", methods=["GET"])
def main_route():
    hostname="select DISTINCT host from record;"
    username="select DISTINCT username from record;"
    password="select DISTINCT password from record;"
    db_names="select DISTINCT dbnames from record;"
    tool="select DISTINCT tool from record;"
    status="select DISTINCT status from record;"
    isActive="select DISTINCT isActive from record;"
    everything="select * from record;"


    print(hostname)


    data = db.session.execute(hostname)
    data_1 = db.session.execute(username)
    data_2 = db.session.execute(password)
    data_3 = db.session.execute(db_names)
    data_4 = db.session.execute(tool)
    data_5 = db.session.execute(status)
    data_6 = db.session.execute(isActive)

    print (data)
    message = "success"
    result = deployments_schema.dump(data) 
    result_1 = deployments_schema.dump(data_1) 
    #result_2 = deployments_schema.dump(data_2) 
    result_3 = deployments_schema.dump(data_3) 
    result_4 = deployments_schema.dump(data_4) 
    result_5 = deployments_schema.dump(data_5) 
    result_6 = deployments_schema.dump(data_6)

    append_1 = {"host": "all"}
    append_2 = {"dbnames": "all"}
    append_3 = {"tool": "all"}
    append_4 = {"username": "all"}
    append_5 = {"status": "all"}
    append_6 = {"isActive": "all"}

    print ("Result is:", result)
    for row in result:
        print("Row is:", row['host'])

    #data = db.session.execute(everything)
    #result = deployments_schema.dump(data) 
    result.insert(0,append_1)
    result_3.insert(0,append_2)
    result_4.insert(0,append_3)
    result_1.insert(0,append_4)
    result_5.insert(0,append_5)
    result_6.insert(0,append_6)
    print ("Result is:", result)
    #return components
    #return render_template("index.html", host_names=result)
    #return render_template("index.html", host_names=result, user_name=result_1, password=result_2, db_names=result_3, tool=result_4)
    return render_template("index.html", host_names=result, user_name=result_1, db_names=result_3, tool=result_4, status=result_5, isActive=result_6)
  



@app.route("/summ", methods=['GET', 'POST'])
def summ():
    x="Hello"
    query = f"select id,host,username,dbnames,tool,status,isActive,expiry,created_at from `record`;"
    print(query)
    data = db.session.execute(query)
    message = "success"
    result = deployments_schema.dump(data)
    print (result)
    column_order = ["id", "host", "username", "dbnames", "tool", "status","isActive", "expiry","created_at"]
    ordered_result = [OrderedDict((col, item[col]) for col in column_order) for item in result]
    table_data = json2html.convert(json=ordered_result, table_attributes="id=\"info-table\" class=\"table table-bordered table-hover\"")
    #table_data = (json2html.convert(json = result, table_attributes="id=\"info-table\" class=\"table table-bordered table-hover\""))
    return render_template("table.html", table_data=table_data)
    #return x


@app.route("/test" , methods=['GET', 'POST'])
def test():
    x="Hello"
    hostname = request.form.get('comp')
    username = request.form.get('sub_comp') 
    tool =  request.form.get('tool')
    db_names = request.form.get('release')

    status =  request.form.get('status')
    isActive = request.form.get('isActive')
    print ("isactive is:", isActive)
    print (hostname,username,tool,db_names)
    if hostname and hostname.lower() == "all":
        hostname = "%"
    if db_names and db_names.lower() == "all":
        db_names = "%"
    if tool and tool.lower() == "all":
        tool = "%"
    if username and username.lower() == "all":
        username = "%"

    if status and status.lower() == "all":
        status = "%"

    if isActive and isActive.lower() == "all":
        isActive = "%"

    print ("I am in else condition")

    print ("After change", hostname,username,tool,db_names,username,status,isActive)
    #query = f"select id,host,username,dbnames,tool,status,isActive,created_at from `record` where dbnames LIKE '%{db_names}%' and host LIKE '%{hostname}%' and username LIKE '%{username}%' and tool LIKE '%{tool}%' and status LIKE '%{status}%' and isActive='%{isActive}%';"
    
    #query = f"select id,host,username,dbnames,tool,status,isActive,created_at from `record` where dbnames LIKE '%{db_names}%' and host LIKE '%{hostname}%' and username LIKE '%{username}%' and tool LIKE '%{tool}%' and status='{status}' and isActive='{isActive}';"
              #select id,host,username,dbnames,tool,status,isActive,created_at from `record` where dbnames LIKE '%prod%' and host LIKE '%%%' and username LIKE '%%%' and tool LIKE '%%%' and status='active' and isActive='1'
    query = f"select id,host,username,dbnames,tool,status,isActive,expiry,created_at from `record` where dbnames LIKE '%{db_names}%' and host LIKE '%{hostname}%' and username LIKE '%{username}%' and tool LIKE '%{tool}%' and status LIKE '%{status}%' and isActive LIKE '%{isActive}%';"
     
    print (hostname,username,tool,db_names)
    print(query)
    data = db.session.execute(query)
    message = "success"
    result = deployments_schema.dump(data)
    print (result)
    column_order = ["id", "host", "username", "dbnames", "tool", "status", "isActive", "expiry", "created_at"]
    ordered_result = [OrderedDict((col, item[col]) for col in column_order) for item in result]   
    table_data = (json2html.convert(json = ordered_result, table_attributes="id=\"info-table\" class=\"table table-bordered table-hover\""))
    return render_template("table.html", table_data=table_data)
    #return x



@app.route("/ranges", methods=['GET', 'POST'])
def ranges():
    from_date = request.form.get('from_date')
    to_date = request.form.get('to_date')
    print ("From Date is:", from_date)
    print ("To Date is:", to_date)
    try:
        from_format = from_date.split('-')
        day_from = from_format[2]
        month_from = from_format[1]
        year_from = from_format[0]
        #correct_format_from = f"{day_from}-{month_from}-{year_from}"
        correct_format_from = f"{year_from}-{month_from}-{day_from}"
        print("Correct Format From is:", correct_format_from)  
    except:
        print ("Except of from date")
        correct_format_from = ""
        print (correct_format_from)
    try:
        to_format = to_date.split('-')
        day_to = to_format[2]
        month_to = to_format[1]
        year_to = to_format[0]
        #correct_format_to = f"{day_to}-{month_to}-{year_to}"
        correct_format_to = f"{year_to}-{month_to}-{day_to}"
        print("Correct Format To is:", correct_format_to) 
    except:
        print ("Except of To date")
        correct_format_to = ""
        print (correct_format_to)
    
    query = f"SELECT id,host,username,dbnames,tool,status,isActive,expiry,created_at FROM `record` where created_at between '{correct_format_from}' and '{correct_format_to}';"
    print(query)
    data = db.session.execute(query)
    result = deployments_schema.dump(data)
    column_order = ["id", "host", "username", "dbnames", "tool", "status", "isActive","expiry","created_at"]
    ordered_result = [OrderedDict((col, item[col]) for col in column_order) for item in result]   
    table_data = (json2html.convert(json = ordered_result, table_attributes="id=\"info-table\" class=\"table table-bordered table-hover\""))
    return render_template("table.html", table_data=table_data)
