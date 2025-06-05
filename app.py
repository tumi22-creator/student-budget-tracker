from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB_NAME = 'budget.db'

# Create table if not exists
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT,
                amount REAL,
                description TEXT,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

@app.route('/')
def index():
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM transactions ORDER BY date DESC")
        transactions = cur.fetchall()
        cur.execute("SELECT SUM(CASE WHEN type='income' THEN amount ELSE -amount END) FROM transactions")
        balance = cur.fetchone()[0] or 0
    return render_template('index.html', transactions=transactions, balance=balance)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        t_type = request.form['type']
        amount = float(request.form['amount'])
        desc = request.form['description']
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute("INSERT INTO transactions (type, amount, description) VALUES (?, ?, ?)",
                         (t_type, amount, desc))
        return redirect(url_for('index'))
    return render_template('add.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
