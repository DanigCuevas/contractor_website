# imports
from flask import Flask, request, make_response, render_template
from flask_sqlalchemy import SQLAlchemy

# initializing Flask app
website = Flask(__name__)


# Google Cloud SQL (change this accordingly)
PASSWORD ="VMUV}?H%Zd9#YtLk"
PUBLIC_IP_ADDRESS ="35.223.51.83"
DBNAME ="contractor-app"
PROJECT_ID ="cogent-jetty-379521"
INSTANCE_NAME ="Contractor App"

# website.config["SECRET_KEY"] = "yoursecretkey"
website.config["SQLALCHEMY_DATABASE_URI"]= f"mysql + mysqldb://root:{PASSWORD}@{PUBLIC_IP_ADDRESS}/{DBNAME}?unix_socket =/cloudsql/{PROJECT_ID}:{INSTANCE_NAME}"
website.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= True

db = SQLAlchemy(website)

@app.route('/')
def home():
   return render_template('home.html')
if __name__ == '__main__':
   website.run()