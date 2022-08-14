from flask import Flask, render_template,request
from flask_mysqldb import MySQL
from numpy import kaiser
import yfinance as yf
import jinja2 as jn
import json
import jsonify

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] = 'newsql'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


@app.route("/",methods = ['POST','GET'])
def hello_world():
    if request.method == 'POST':
        print(request.get_json())
        req=request.get_json()
        return {"result":req["company"]}
    paragraph = "script to view stocks in a convienent way"
    return {"app_name": "Stock_data"}


@app.route("/stocks/<company>")
def stocks(company):
    msft = yf.Ticker(company)
    print(msft.info)
    return render_template("company.html",company = msft.info) 

@app.route("/stocks/<company>/dividens") #create a html doc for dividens
def dividens(company):
    company_details = yf.Ticker(company)
    dividends = company_details.dividends.tolist()
    print(dividends)
    return render_template("dividends.html" ,dividends = dividends)
@app.route("/users",methods = ['POST','GET'])
def get_users():
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM users''')
    users = cursor.fetchall()
    print(users)
    userjson= json.dumps(users)
    return userjson
@app.route("/products",methods = ['GET','POST','PUT'])
def products():
    if request.method == 'POST':
        requestjson = request.get_json()       
        Productname = requestjson['Productname']
        Quantity = requestjson['Quantity']
        Price = requestjson['Price']
        #id = requestjson['id']
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO Products(Productname,Quantity,Price) VALUES (%s,%s,%s)" ,(Productname,Quantity,Price))  
        mysql.connection.commit()
        return "True"   
    elif request.method == 'PUT':
        requestjson = request.get_json()       
        Productname = requestjson['Productname']
        Quantity = requestjson['Quantity']
        Price = requestjson['Price']
        id = requestjson['id']
        cursor = mysql.connection.cursor()
        cursor.execute("""UPDATE Products SET Productname=%s, Quantity=%s, Price=%s WHERE id=%s""", (Productname, Quantity, Price, id))
        mysql.connection.commit()
        return "updated sucessfully"
        
    else:
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT * FROM Products WHERE isDeleted = 0''')
        users = cursor.fetchall()
        print(users)
        userjson = json.dumps(users)
        return userjson
@app.route("/products/<id>",methods = ['POST','GET'])
def single_product(id):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM Products WHERE id = {}".format(id)
    cursor.execute(query)
    users = cursor.fetchone()
    print(users)
    userjson= json.dumps(users)
    return userjson
@app.route("/products/<id>",methods = ['DELETE'])
def delete_product(id):
    #requestjson = request.get_json()
    #id = requestjson['id']
    cursor = mysql.connection.cursor()
    query = "UPDATE Products SET isDeleted = 1 WHERE id = {}".format(id)
    print(query)
    cursor.execute(query)
    mysql.connection.commit()
    users = cursor.fetchone()
    print(users)
    userjson= json.dumps(users)
    return userjson
 
    # "UPDATE Products SET isDeleted = 1"
    # query = ""
    
    
    #make isDeleted = true after running id through
