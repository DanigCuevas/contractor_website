# imports

from google.cloud.sql.connector import Connector
import pymysql
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

# initializing Flask app
app = Flask(__name__)

# initialize Connector object
connector = Connector()

# Google Cloud SQL 
PASSWORD ="VMUV}?H%Zd9#YtLk"
PUBLIC_IP_ADDRESS ="35.223.51.83"
DBNAME ="contractor-app"
PROJECT_ID ="cogent-jetty-379521"
INSTANCE_NAME ="Contractor App"

# website.config["SECRET_KEY"] = "yoursecretkey"
app.config["SQLALCHEMY_DATABASE_URI"]= f"mysql+mysqldb://root:{PASSWORD}@{PUBLIC_IP_ADDRESS}/{DBNAME}?unix_socket =/cloudsql/{PROJECT_ID}:{INSTANCE_NAME}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= True


# function to return the database connection
def getconn() -> pymysql.connections.Connection:
    conn: pymysql.connections.Connection = connector.connect(
        "cogent-jetty-379521:us-central1:contractor-app",
        "pymysql",
        user="ContractorApp",
        password="VMUV}?H%Zd9#YtLk",
        db="contractor-app"
    )
    return conn

db = SQLAlchemy(app)

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