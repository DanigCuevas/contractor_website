# imports

import os
import pymysql
from flask import Flask, render_template,request, url_for, flash, redirect
from werkzeug.exceptions import abort

# initializing Flask app
app = Flask(__name__)

#this might have to be included for deploying the project
db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

#this connection style might be needed for connnection
@app.route('/')
def main():
    # When deployed to App Engine, the `GAE_ENV` environment variable will be
    # set to `standard`
    if os.environ.get('GAE_ENV') == 'standard':
        # If deployed, use the local socket interface for accessing Cloud SQL
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name)
    else:
        # If running locally, use the TCP connections instead
        # Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
        # so that your application can use 127.0.0.1:3306 to connect to your
        # Cloud SQL instance
        host = '127.0.0.1'
        cnx = pymysql.connect(user=db_user, password=db_password,
                              host=host, db=db_name)

    viewCustomer(cnx)
    # with cnx.cursor() as db_conn:
    #     query = "SELECT * FROM CUSTOMER"
    #     db_conn.execute(query)
    #     customers = db_conn.fetchall()
    #     cnx.close()
    #     return render_template('home.html',customers=customers)

def viewCustomer(cnx):
    with cnx.cursor() as db_conn:
        query = "SELECT * FROM CUSTOMER"
        db_conn.execute(query)
        customers = db_conn.fetchall()
        cnx.close()
        return render_template('home.html',customers=customers)



#function to render the home page
@app.route('/')
def home():
   return render_template('home.html')

@app.route("/login")
def login():
  return render_template("login.html")

@app.route("/job")
def job():
  return render_template("job.html")

@app.route("/contractorReviews")
def contractorReviews():
  return render_template("contractorReviews.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)