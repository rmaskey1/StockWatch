import psycopg2
from datetime import timedelta
from flask import Flask, request, send_file, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "stockwatch"

conn = psycopg2.connect(
    host="localhost",
    database="StockWatch",
    user="postgres",
    password="admin"
)

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=0.1)

@app.route('/', methods=['POST', 'GET'])
def home():
    if "username" in session:
        return render_template("home.html")
    else:
        return redirect(url_for("login"))

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        # Get form data
        username = request.form['username']
        password = request.form['password']

        # Insert data into the database
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM "user" WHERE username = %s', (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            cursor.execute('SELECT password FROM "user" WHERE username = %s', (username,))
            pswd = cursor.fetchone()
            if password == pswd[0]:
                session["username"] = username
                cursor.close()
                return redirect(url_for("home"))
            else:
                cursor.close()
                return render_template("login.html", error=True)
        else:
            cursor.close()
            return render_template("login.html", error=True)
    else:
        return render_template("login.html", error=False)

@app.route('/logout')
def logout():
    session.pop("username")
    return redirect(url_for("login"))

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == "POST":
        # Get form data
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Insert data into the database
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM "user" WHERE username = %s', (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            return render_template("signup.html", error=True)
        else:
            cursor.execute('INSERT INTO watchlist (stock_id) VALUES (%s)', (1,))
            cursor.execute('INSERT INTO "user" (username, password, email) VALUES (%s, %s, %s)', (username, password, email))
            conn.commit()
            cursor.close()
            return redirect(url_for("login"))
    else:
        return render_template("signup.html", error=False)

if __name__ == '__main__':
    session.clear()
    app.debug = True
    app.run()