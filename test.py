import psycopg2
from flask import Flask, request, send_file, render_template, redirect, url_for, session

conn = psycopg2.connect(
    host="localhost",
    database="Test",
    user="postgres",
    password="admin"
)

cursor = conn.cursor()
username = "reshaj!"
cursor.execute('SELECT password FROM "user" WHERE username = %s', (username,))
existing_user = cursor.fetchone()
print(existing_user[0])