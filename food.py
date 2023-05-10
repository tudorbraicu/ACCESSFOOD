import sqlite3
from flask import Flask, render_template

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('food.db')
    conn.row_factory = sqlite3.Row
    return conn
