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
@app.route("/job") #THIS NEEDS TO BE FIXED
def job():
    cnx = getConn()
    jobQuery = "SELECT job.service_type, customer.customer_name, contractor.contractor_name, job.job_time, job.job_date\
                FROM Job, Contractor, Customer \
                WHERE customer.customer_ID = job.customer_ID \
                AND contractor.contractor_ID = job.Contractor_ID\
                AND job.service_type = landscaping AND customer.customer_id = 603753 "
        #note serv_type should be landscaping  and cust_id should be 603753
    # jobQuery = jobQuery.bindparams(serv_type="landscaping", cust_id=603753)
    jobs = getQuery(cnx,jobQuery)
    cnx.close ()
    return render_template("job.html",jobs=jobs)


#you can create another html file for the sendsEnquiry & use that to show enquiry query 
@app.route("/contractorReviews")
def contractorReviews():
    #need to do this query
    #SELECT customer_rates_contractor.score, customer_rates_contractor.rating_date, customer_rates_contractor.rating_time, Customer.customer_name, Contractor.contractor_name, customer_rates_contractor.rating_comment
    #  FROM Customer, Contractor, Job, Customer_rates_contractor 
    # WHERE customer.customer_ID = job.customer_ID AND job.contractor_ID = contractor.contractor_ID AND job.job_ID = customer_rates_contractor.job_ID and customer.customer_ID = '603753' AND  job.job_ID = '152697';
  return render_template("contractorReviews.html")

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