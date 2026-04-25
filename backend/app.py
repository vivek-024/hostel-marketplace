import os
import sqlite3
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# IMAGE CONFIG
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# DATABASE CONNECTION
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# CREATE TABLES (auto-run once)
def init_db():
    conn = get_db_connection()
    
    conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        password TEXT
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT,
        price REAL,
        type TEXT,
        owner_id INTEGER,
        image TEXT,
        deposit REAL
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        buyer_id INTEGER,
        product_id INTEGER
    )
    """)

    conn.commit()
    conn.close()

# Run DB init
init_db()

@app.route('/')
def home():
    return "Backend is running!"

# REGISTER
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
        (data['name'], data['email'], data['password'])
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "User registered successfully"})

# LOGIN
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    conn = get_db_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (data['email'], data['password'])
    ).fetchone()
    conn.close()

    if user:
        return jsonify({"message": "Login successful", "user_id": user["id"]})
    else:
        return jsonify({"message": "Invalid credentials"}), 401

# ADD PRODUCT
@app.route('/add-product', methods=['POST'])
def add_product():
    title = request.form['title']
    description = request.form['description']
    price = request.form['price']
    owner_id = request.form['owner_id']
    type_ = request.form.get('type', 'sell')
    deposit = request.form.get('deposit', 0)

    file = request.files['image']
    filename = secure_filename(file.filename)

    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    conn = get_db_connection()
    conn.execute("""
        INSERT INTO products 
        (title, description, price, type, owner_id, image, deposit)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (title, description, price, type_, owner_id, filename, deposit))
    conn.commit()
    conn.close()

    return jsonify({"message": "Product added successfully"})

# GET PRODUCTS
@app.route('/products', methods=['GET'])
def get_products():
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM products").fetchall()
    conn.close()

    products = []
    for row in rows:
        products.append({
            "id": row["id"],
            "title": row["title"],
            "description": row["description"],
            "price": row["price"],
            "type": row["type"],
            "owner_id": row["owner_id"],
            "image": row["image"],
            "deposit": row["deposit"]
        })

    return jsonify(products)

# REQUEST PRODUCT
@app.route('/request-product', methods=['POST'])
def request_product():
    data = request.json
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO requests (buyer_id, product_id) VALUES (?, ?)",
        (data['buyer_id'], data['product_id'])
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Request sent successfully"})

# SERVE IMAGES
@app.route('/uploads/<filename>')
def get_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# RUN APP
if __name__ == '__main__':
    app.run(debug=True)import os
import sqlite3
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# IMAGE CONFIG
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# DATABASE CONNECTION
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# CREATE TABLES (auto-run once)
def init_db():
    conn = get_db_connection()
    
    conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        password TEXT
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT,
        price REAL,
        type TEXT,
        owner_id INTEGER,
        image TEXT,
        deposit REAL
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        buyer_id INTEGER,
        product_id INTEGER
    )
    """)

    conn.commit()
    conn.close()

# Run DB init
init_db()

@app.route('/')
def home():
    return "Backend is running!"

# REGISTER
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
        (data['name'], data['email'], data['password'])
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "User registered successfully"})

# LOGIN
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    conn = get_db_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (data['email'], data['password'])
    ).fetchone()
    conn.close()

    if user:
        return jsonify({"message": "Login successful", "user_id": user["id"]})
    else:
        return jsonify({"message": "Invalid credentials"}), 401

# ADD PRODUCT
@app.route('/add-product', methods=['POST'])
def add_product():
    title = request.form['title']
    description = request.form['description']
    price = request.form['price']
    owner_id = request.form['owner_id']
    type_ = request.form.get('type', 'sell')
    deposit = request.form.get('deposit', 0)

    file = request.files['image']
    filename = secure_filename(file.filename)

    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    conn = get_db_connection()
    conn.execute("""
        INSERT INTO products 
        (title, description, price, type, owner_id, image, deposit)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (title, description, price, type_, owner_id, filename, deposit))
    conn.commit()
    conn.close()

    return jsonify({"message": "Product added successfully"})

# GET PRODUCTS
@app.route('/products', methods=['GET'])
def get_products():
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM products").fetchall()
    conn.close()

    products = []
    for row in rows:
        products.append({
            "id": row["id"],
            "title": row["title"],
            "description": row["description"],
            "price": row["price"],
            "type": row["type"],
            "owner_id": row["owner_id"],
            "image": row["image"],
            "deposit": row["deposit"]
        })

    return jsonify(products)

# REQUEST PRODUCT
@app.route('/request-product', methods=['POST'])
def request_product():
    data = request.json
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO requests (buyer_id, product_id) VALUES (?, ?)",
        (data['buyer_id'], data['product_id'])
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Request sent successfully"})

# SERVE IMAGES
@app.route('/uploads/<filename>')
def get_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# RUN APP
if __name__ == '__main__':
    app.run(debug=True)