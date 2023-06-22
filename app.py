from flask import Flask, send_file, request, redirect, session
import psycopg2

app = Flask(__name__)

@app.route('/')
def index():
    return send_file('login.html')