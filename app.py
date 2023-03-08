# imports

from google.cloud.sql.connector import Connector, IPTypes
import pymysql
from flask import Flask, request, make_response, render_template
from flask_sqlalchemy import SQLAlchemy

# initializing Flask app
website = Flask(__name__)


# Google Cloud SQL 
PASSWORD ="VMUV}?H%Zd9#YtLk"
PUBLIC_IP_ADDRESS ="35.223.51.83"
DBNAME ="contractor-app"
PROJECT_ID ="cogent-jetty-379521"
INSTANCE_NAME ="Contractor App"

# website.config["SECRET_KEY"] = "yoursecretkey"
website.config["SQLALCHEMY_DATABASE_URI"]= f"mysql+mysqldb://root:{PASSWORD}@{PUBLIC_IP_ADDRESS}/{DBNAME}?unix_socket =/cloudsql/{PROJECT_ID}:{INSTANCE_NAME}"
website.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= True

# initialize Connector object
connector = Connector()

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

db = SQLAlchemy(website)

@website.route("/")
def viewCustomers():
    #query customers
    conn = getconn()

    customers = conn.excute("SELECT * FROM CUSTOMER").fetchall()
    conn.close()
    return render_template('home.html',customers=customers)



#function to render the home page
@website.route('/')
def home():
   return render_template('home.html')

if __name__ == '__main__':
   website.run()