from flask import Flask, render_template, request, redirect, session
import mysql.connector


app = Flask(__name__)
app.secret_key = "your_secret_key"


def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="DB"
    )
    return connection


conn = get_db_connection()

cursor = conn.cursor()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route('/registerRegister', methods=['POST'])
def registerRegister():
    input1 = request.form['navn']
    input3 = request.form['passord']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (navn, passord) VALUES (%s, %s)", (input1, input3))
    conn.commit()
    cursor.close()
    conn.close()
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        text = request.form['navn']
        password = request.form['passord']
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE navn = %s AND passord = %s", (text, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['user_name'] = user['navn']
            return redirect('/main')
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route("/order")
def order():
    return render_template("order.html")

if __name__ == "__main__":
    app.run(debug=True)
