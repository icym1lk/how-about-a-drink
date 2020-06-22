import requests
# import Flask and any libraries you want to use
from flask import Flask, request, jsonify, render_template, redirect, flash, session
# get db related stuff from models.py
from models import db, connect_db

# instantiate and instance of Flask. app is standard name
app = Flask(__name__)

# connect to db
connect_db(app)