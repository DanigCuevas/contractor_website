# imports

from google.cloud.sql.connector import Connector
import pymysql
import os
from flask import Flask, render_template,request, url_for, flash, redirect
from werkzeug.exceptions import abort
from flask_sqlalchemy import SQLAlchemy

# initializing Flask app
app = Flask(__name__)

# initialize Connector object
connector = Connector()

#this might have to be included for deploying the project
# db_user = os.environ.get('CLOUD_SQL_USERNAME')
# db_password = os.environ.get('CLOUD_SQL_PASSWORD')
# db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
# db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

# Google Cloud SQL 
PASSWORD ="VMUV}?H%Zd9#YtLk"
PUBLIC_IP_ADDRESS ="35.223.51.83"
DBNAME ="contractor-app"
PROJECT_ID ="cogent-jetty-379521"
INSTANCE_NAME ="Contractor App"

# website.config["SECRET_KEY"] = "yoursecretkey"
app.config["SQLALCHEMY_DATABASE_URI"]= f"mysql+mysqldb://root:{PASSWORD}@{PUBLIC_IP_ADDRESS}/{DBNAME}?unix_socket =/cloudsql/{PROJECT_ID}:{INSTANCE_NAME}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= True



# function to return the database connection locally
def getconn() -> pymysql.connections.Connection:
    conn: pymysql.connections.Connection = connector.connect(
        "cogent-jetty-379521:us-central1:contractor-app",
        "pymysql",
        user="ContractorApp",
        password="VMUV}?H%Zd9#YtLk",
        db="contractor-app"
    )
    return conn


#this connection style might be needed for connnection
# @app.route('/') 
# def main():
#     # When deployed to App Engine, the `GAE_ENV` environment variable will be
#     # set to `standard`
#     if os.environ.get('GAE_ENV') == 'standard':
#         # If running locally, use the TCP connections instead
#         # Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
#         # so that your application can use 127.0.0.1:3306 to connect to your
#         # Cloud SQL instance
#         host = '172.23.16.3'
#         cnx = pymysql.connect(user=db_user, password=db_password,
#                               host=host, db=db_name)
#     else:
#         # If deployed, use the local socket interface for accessing Cloud SQL
#         unix_socket = '/cloudsql/{}'.format(db_connection_name)
#         cnx = pymysql.connect(user=db_user, password=db_password,
#                               unix_socket=unix_socket, db=db_name)

#     with cnx.cursor() as cursor:
#         cursor.execute('select demo_txt from demo_tbl;')
#         result = cursor.fetchall()
#         current_msg = result[0][0]
#     cnx.close()

#     return str(current_msg)

db = SQLAlchemy(app)

#view all customers
@app.route("/")
def viewCustomers():
    #query customers
    conn = getconn()

    with conn.cursor() as db_conn:
        query = "SELECT * FROM CUSTOMER"
        db_conn.execute(query)
        customers = db_conn.fetchall()
        conn.close()
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
   app.run(debug=True, port=8080)