from flask import Flask, request, render_template, jsonify, redirect, url_for
import sqlite3
import csv
import io
import os

DB = os.path.join(os.path.dirname(__file__), 'skus.db')

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS skus (
        id INTEGER PRIMARY KEY,
        sku TEXT UNIQUE,
        description TEXT,
        stock INTEGER
    )
    ''')
    conn.commit()
    conn.close()

def insert_sku(sku, description, stock):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    try:
        c.execute('INSERT OR REPLACE INTO skus (sku, description, stock) VALUES (?, ?, ?)',
                  (sku, description, stock))
        conn.commit()
    finally:
        conn.close()

def find_sku_exact(sku):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('SELECT sku, description, stock FROM skus WHERE sku = ?', (sku,))
    row = c.fetchone()
    conn.close()
    return row

def find_sku_partial(sku):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    pattern = f"%{sku}%"
    c.execute('SELECT sku, description, stock FROM skus WHERE sku LIKE ? LIMIT 10', (pattern,))
    rows = c.fetchall()
    conn.close()
    return rows

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    f = request.files['file']
    stream = io.StringIO(f.stream.read().decode('utf-8'))
    reader = csv.DictReader(stream)
    count = 0
    for row in reader:
        sku = row.get('sku') or row.get('SKU') or row.get('Sku')
        desc = row.get('description') or row.get('desc') or ''
        stock = row.get('stock') or row.get('qty') or '0'
        try:
            stock_int = int(stock)
        except Exception:
            stock_int = 0
        if sku:
            insert_sku(sku.strip(), desc.strip(), stock_int)
            count += 1
    return jsonify({'status': 'ok', 'imported': count})

@app.route('/triage', methods=['POST'])
def triage():
    data = request.get_json() or {}
    sku = data.get('sku', '').strip()
    if not sku:
        return jsonify({'error': 'sku requerido'}), 400

    exact = find_sku_exact(sku)
    if exact:
        sku_val, desc, stock = exact
        return jsonify({'result': 'exact', 'sku': sku_val, 'description': desc, 'stock': stock})

    partials = find_sku_partial(sku)
    if partials:
        results = [{'sku': r[0], 'description': r[1], 'stock': r[2]} for r in partials]
        return jsonify({'result': 'partial', 'matches': results})

    return jsonify({'result': 'not_found'})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
