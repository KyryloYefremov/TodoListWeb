from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
db = SQLAlchemy()
bootstrap = Bootstrap5(app)
# Create database
db_file_name = "task-manager.db"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_file_name}"
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
# Initialise the app with the extension
db.init_app(app)
