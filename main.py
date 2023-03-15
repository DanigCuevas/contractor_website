# imports

import os
import pymysql
import sqlalchemy
from sqlalchemy import text
from flask import Flask, render_template,request, url_for, flash, redirect
from werkzeug.exceptions import abort

# initializing Flask app
app = Flask(__name__)


#database google cloud information
db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

#Retrieves connection to database
def getConn():
    # run in google enginge environment
    if os.environ.get('GAE_ENV') == 'standard':
        # If deployed, use the local socket interface for accessing Cloud SQL
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name)
        return cnx
    else:
        # If running locally, use the TCP connections instead
        # Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
        # so that your application can use 127.0.0.1:3306 to connect to your
        # Cloud SQL instance
        host = '127.0.0.1'
        cnx = pymysql.connect(user=db_user, password=db_password,
                              host=host, db=db_name) 
        return  cnx                          
    # with cnx.cursor() as db_conn:
    #     query = "SELECT * FROM CUSTOMER"
    #     db_conn.execute(query)
    #     customers = db_conn.fetchall()
    #     cnx.close()
    #     return render_template('home.html',customers=customers)
    
#executes a query from the database 
def getQuery(cnx,query):
    with cnx.cursor() as db_conn:   
        db_conn.execute(query)
        results = db_conn.fetchall()
        return results

#sends query results to home page
@app.route('/')
def home():
    #retrive database connection
    cnx = getConn() 
    #execute query
    contactorQuery = "SELECT * FROM CONTRACTOR"
    contractors = getQuery(cnx,contactorQuery)
    #close connection
    cnx.close ()
    return render_template('home.html',contractors=contractors)

#sends query results to login page
@app.route("/login")
def login():
  cnx = getConn()
  customerQuery = "SELECT * FROM CUSTOMER WHERE CUSTOMER.customer_ID = 603753"
  customers = getQuery(cnx,customerQuery)
  cnx.close ()
  return render_template("login.html",customers=customers)

#send job query to job page
@app.route("/job") #Fixed! (the error was because MySQL is case sensitive)
def job():
    cnx = getConn()
    jobQuery = "SELECT J.service_type, C.customer_name, CON.contractor_name, J.job_time, J.job_date \
                FROM JOB J, CONTRACTOR CON, CUSTOMER C \
                WHERE C.customer_ID = J.customer_ID \
                AND CON.contractor_ID = J.contractor_ID \
                AND J.service_type = \'landscaping\' AND C.customer_id = 603753"
        #note serv_type should be landscaping and cust_id should be 603753
    # jobQuery = jobQuery.bindparams(serv_type="landscaping", cust_id=603753)
    jobs = getQuery(cnx,jobQuery)
    cnx.close()
    return render_template("job.html",jobs=jobs)

#you can create another html file for the sendsEnquiry & use that to show enquiry query 
@app.route("/contractorReviews/<contractorID>")
def contractorReviews(contractorID):
    cnx = getConn()

    #need to do this query
    reviewsQuery = \
        f"SELECT R.score, R.rating_date, R.rating_time, C.customer_name, CON.contractor_name, R.rating_comment \
        FROM CUSTOMER C, CONTRACTOR CON, JOB J, CUSTOMER_RATES_CONTRACTOR R \
        WHERE C.customer_ID = J.customer_ID AND J.contractor_ID = CON.contractor_ID AND \
        J.job_ID = R.job_ID and CON.contractor_ID = {contractorID};"

    reviews = getQuery(cnx, reviewsQuery)
    cnx.close()
    return render_template("contractorReviews.html",reviews=reviews)

# @app.route('/')
# def main():
#     cnx = getConn()

#     home(cnx)
#     login(cnx)
#     job(cnx)
#     view = 'home'
    # if(view == 'home'):
    # contactorQuery = "SELECT * FROM CONTRACTOR"
    # contractors = getQuery(cnx,contactorQuery,view)
    # cnx.close ()
    # home(contractors)
        # return render_template('home.html',contractors=contractors)
    # view = 'Login'
    # if (view == "login"):
    # customerQuery = "SELECT * FROM CUSTOMER WHERE CUSTOMER.customer_ID = 603753"
    # customers = getQuery(cnx,customerQuery,view)
    # cnx.close ()
    # return render_template('login.html',customers=customers)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)