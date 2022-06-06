from flask import Flask, render_template,request
import yfinance as yf
import jinja2 as jn
app = Flask(__name__)

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

  

