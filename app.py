import os
from datetime import datetime
from flask import Flask, request, render_template_string
import psycopg2

app = Flask(__name__)

DB_USER = os.environ.get("DB_USER", "admin")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "secret")
DB_NAME = os.environ.get("DB_NAME", "mydb")
DB_HOST = os.environ.get("DB_HOST", "db")

def get_db():
    return psycopg2.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        dbname=DB_NAME
    )

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT NOW()
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

@app.route("/")
def home():
    return "DevOps Engineer Portfolio"

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)",
            (name, email, message)
        )
        conn.commit()
        cur.close()
        conn.close()
        return "Message saved!"
    return render_template_string("""
        <form method='POST'>
            Name: <input type='text' name='name'><br>
            Email: <input type='email' name='email'><br>
            Message: <textarea name='message'></textarea><br>
            <input type='submit' value='Send'>
        </form>
    """)

@app.route("/messages")
def messages():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT name, email, message, created_at FROM contacts ORDER BY created_at DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    result = "<h2>Messages</h2>"
    for r in rows:
        result += f"<p><b>{r[0]}</b> ({r[1]}): {r[2]} <i>{r[3]}</i></p>"
    return result

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
