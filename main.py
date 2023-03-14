# imports

import os
import pymysql
import sqlalchemy
from flask import Flask, render_template,request, url_for, flash, redirect
from werkzeug.exceptions import abort

# initializing Flask app
app = Flask(__name__)

#database
# db = None

#database google cloud information
db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

# @app.route('/')
def getconn():
    db_config = {
        # [START cloud_sql_mysql_sqlalchemy_limit]
        # Pool size is the maximum number of permanent connections to keep.
        "pool_size": 1,
        # Temporarily exceeds the set pool_size if no connections are available.
        "max_overflow": 0,
        # The total number of concurrent connections for your application will be
        # a total of pool_size and max_overflow.
        # [END cloud_sql_mysql_sqlalchemy_limit]

        # [START cloud_sql_mysql_sqlalchemy_backoff]
        # SQLAlchemy automatically uses delays between failed connection attempts,
        # but provides no arguments for configuration.
        # [END cloud_sql_mysql_sqlalchemy_backoff]

        # [START cloud_sql_mysql_sqlalchemy_timeout]
        # 'pool_timeout' is the maximum number of seconds to wait when retrieving a
        # new connection from the pool. After the specified amount of time, an
        # exception will be thrown.
        "pool_timeout": 30,  # 30 seconds
        # [END cloud_sql_mysql_sqlalchemy_timeout]

        # [START cloud_sql_mysql_sqlalchemy_lifetime]
        # 'pool_recycle' is the maximum number of seconds a connection can persist.
        # Connections that live longer than the specified amount of time will be
        # reestablished
        "pool_recycle": 1800,  # 30 minutes
        # [END cloud_sql_mysql_sqlalchemy_lifetime]

    }
    return connect_unix_socket(db_config)

def connect_unix_socket(db_config):
    # """ Initializes a Unix socket connection pool for a Cloud SQL instance of MySQL. """
    # Note: Saving credentials in environment variables is convenient, but not
    pool = sqlalchemy.create_engine(
        # Equivalent URL:
        # mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=<socket_path>/<cloud_sql_instance_name>
        sqlalchemy.engine.url.URL.create(
            drivername="mysql+pymysql",
            username=db_user,
            password=db_password,
            database=db_name,
            query= {"unix_socket": "{}/{}".format(
                    "/cloudsql", 
                    db_connection_name) 
                }
            # {"unix_socket": unix_socket_path},
        ),
    )
    return pool


def view_Customer():
    cnx = getconn()
    with cnx.connect() as db_conn:
        query = "SELECT * FROM CUSTOMER"
        db_conn.execute(query)
        customers = db_conn.fetchall()
        cnx.close()
        return render_template('home.html',customers=customers)

#Retrieves connection to database => this works 
# @app.route('/')
# def get_Conn():
#     # When deployed to App Engine, the `GAE_ENV` environment variable will be
#     # set to `standard`
#     if os.environ.get('GAE_ENV') == 'standard':
#         # If deployed, use the local socket interface for accessing Cloud SQL
#         unix_socket = '/cloudsql/{}'.format(db_connection_name)
#         cnx = pymysql.connect(user=db_user, password=db_password,
#                               unix_socket=unix_socket, db=db_name)
#     else:
#         # If running locally, use the TCP connections instead
#         # Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
#         # so that your application can use 127.0.0.1:3306 to connect to your
#         # Cloud SQL instance
#         host = '127.0.0.1'
#         cnx = pymysql.connect(user=db_user, password=db_password,
#                               host=host, db=db_name)                           
#     with cnx.cursor() as db_conn:
#         query = "SELECT * FROM CUSTOMER"
#         db_conn.execute(query)
#         customers = db_conn.fetchall()
#         cnx.close()
#         return render_template('home.html',customers=customers)
    
    # with cnx.cursor() as db_conn:
    #     query = "SELECT * FROM JOB"
    #     db_conn.execute(query)
    #     jobs = db_conn.fetchall()
    #     cnx.close()
    #     return render_template('job.html',jobs=jobs)


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