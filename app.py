from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "abc"
app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']=""
app.config['MYSQL_DB']="diet"

mysql = MySQL(app)
from routes import *

if __name__ == '__main__':
    app.run(debug=True)
