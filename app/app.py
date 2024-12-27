from flask import Flask, request, jsonify
from datetime import datetime
import psycopg2  # Для PostgreSQL
import os

app = Flask(__name__)


DB_HOST = os.environ.get('DB_HOST', 'db')  # Имя сервиса базы данных в docker-compose
DB_NAME = os.environ.get('DB_NAME', 'counter_db')
DB_USER = os.environ.get('DB_USER', 'user')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'password')

conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)
cur = conn.cursor()

# Создание таблицы при запуске приложения
cur.execute('''
    CREATE TABLE IF NOT EXISTS counter (
        id SERIAL PRIMARY KEY,
        datetime TIMESTAMP,
        client_info TEXT
    )
''')
conn.commit()

@app.route('/increment', methods=['POST'])
def increment():
    client_info = request.headers.get('User-Agent', 'Unknown')
    now = datetime.now()
    cur.execute('INSERT INTO counter (datetime, client_info) VALUES (%s, %s)', (now, client_info))
    conn.commit()
    return jsonify({'message': 'Counter incremented!', 'datetime': now, 'client_info': client_info})

@app.route('/history', methods=['GET'])
def history():
    cur.execute('SELECT * FROM counter')
    rows = cur.fetchall()
    return jsonify(rows)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
