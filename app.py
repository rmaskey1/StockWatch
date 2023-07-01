import psycopg2
from datetime import timedelta
import finnhub
from flask import Flask, request, send_file, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "stockwatch"

conn = psycopg2.connect(
    host="localhost",
    database="StockWatch",
    user="postgres",
    password="admin"
)

finnhub_client = finnhub.Client(api_key="cie9espr01qmfas4b430cie9espr01qmfas4b43g")

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=0.1)

@app.route('/', methods=['POST', 'GET'])
def home():
    if "username" in session:
        username = session["username"]
        cursor = conn.cursor()
        cursor.execute('SELECT user_id FROM "user" where username = %s', (username,))
        user_id = cursor.fetchone()
        cursor.execute('SELECT stock_id FROM watchlist WHERE user_id = %s', (user_id,))
        stock_ids = cursor.fetchall()
        stocks = []
        for stock_id in stock_ids:
            cursor.execute('SELECT * FROM stock WHERE stock_id = %s', (stock_id,))
            stock = cursor.fetchone()
            stocks.append(stock)
        conn.commit()
        cursor.close()
        return render_template("home.html", stocks=stocks)
    else:
        return redirect(url_for("login"))

@app.route('/add', methods=['POST'])
def add():
    if "username" in session and request.method == "POST":
        username = session["username"]
        cursor = conn.cursor()
        cursor.execute('SELECT user_id FROM "user" where username = %s', (username,))
        user_id = cursor.fetchone()
        stock_code = request.form['ticker']
        cursor.execute("SELECT * FROM stock WHERE stock_code = %s", (stock_code,))
        if cursor.fetchone() is not None:
            cursor.execute('SELECT stock_id FROM stock WHERE stock_code = %s', (stock_code,))
            stock_id = cursor.fetchone()
            cursor.execute('INSERT INTO watchlist (user_id, stock_id) VALUES (%s, %s)', (user_id, stock_id,))
            conn.commit()
            cursor.close()
            return redirect(url_for("home"))
        else:
            return redirect(url_for("home"))

@app.route('/delete/<stock_id>', methods=['POST'])
def delete(stock_id):
    if "username" in session:
        username = session["username"]
        cursor = conn.cursor()
        cursor.execute('SELECT user_id FROM "user" where username = %s', (username,))
        user_id = cursor.fetchone()
        cursor.execute('DELETE FROM watchlist WHERE stock_id = %s AND user_id = %s', (stock_id, user_id))
        conn.commit()
        cursor.close()
    return redirect(url_for("home"))

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
            cursor.execute('INSERT INTO "user" (username, password, email) VALUES (%s, %s, %s)', (username, password, email))
            cursor.execute('SELECT user_id FROM "user" where username = %s', (username,))
            user_id = cursor.fetchone()
            cursor.execute('INSERT INTO watchlist (user_id, stock_id) VALUES (%s, %s)', (user_id, 1,))
            conn.commit()
            cursor.close()
            return redirect(url_for("login"))
    else:
        return render_template("signup.html", error=False)

if __name__ == '__main__':
    app.debug = True
    app.run()