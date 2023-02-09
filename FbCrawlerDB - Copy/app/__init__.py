# import os
# from dotenv import load_dotenv
#
# dotenv_path = os.path.join(os.path.dirname(__file__), "../.env")
# if os.path.exists(dotenv_path):
#     load_dotenv(dotenv_path, verbose=True)
#
# # Import flask and template operators
# from flask import Flask
#
# # Import SQLAlchemy
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
#
# # Define the WSGI application object
# flask_app = Flask(__name__)
#
# # Configurations
# BASE_DIR = os.path.abspath(os.curdir)
# flask_app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI") # set config postgres
#
# flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#
# # You need to declare necessary configuration to initialize
# # flask-profiler as follows:
# flask_app.config["flask_profiler"] = {
#     "enabled": True,
#     "storage": {
#         "engine": "sqlalchemy",
#         "db_url": os.environ.get("SQLALCHEMY_DATABASE_URI")
#     },
#     "ignore": [
#         "^/static/.*"
#     ]
# }
#
# # Define the database object which is imported
# # by modules and controllers
# db = SQLAlchemy(flask_app)
# migrate = Migrate(flask_app, db, compare_type=True)
#
# # Import models to create tables
