import os
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify, send_from_directory
# REMOVED: from flask_mysqldb import MySQL (Vercel doesn't support this easily)
from flask_cors import CORS
import config

# ADDED: Compatibility for Vercel/Linux environments
import pymysql
pymysql.install_as_MySQLdb()
from flask_mysqldb import MySQL 

app = Flask(__name__)
CORS(app)

# IMAGE CONFIG
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# MYSQL CONFIG
# These will use your config.py locally and Vercel Environment Variables online
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', config.MYSQL_HOST)
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', config.MYSQL_USER)
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', config.MYSQL_PASSWORD)
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', config.MYSQL_DB)

mysql = MySQL(app)

@app.route('/')
def home():
    return "Backend is running!"

# REGISTER
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
        (data['name'], data['email'], data['password'])
    )
    mysql.connection.commit()
    cur.close()
    return jsonify({"message": "User registered successfully"})

# LOGIN
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT * FROM users WHERE email=%s AND password=%s",
        (data['email'], data['password'])
    )
    user = cur.fetchone()
    cur.close()
    if user:
        return jsonify({"message": "Login successful", "user_id": user[0]})
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
    
    # Ensure upload folder exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
        
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO products 
        (title, description, price, type, owner_id, image, deposit)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """, (title, description, price, type_, owner_id, filename, deposit))
    mysql.connection.commit()
    cur.close()
    return jsonify({"message": "Product added successfully"})

# GET PRODUCTS
@app.route('/products', methods=['GET'])
def get_products():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products")
    data = cur.fetchall()
    products = []
    for row in data:
        products.append({
            "id": row[0], "title": row[1], "description": row[2],
            "price": row[3], "type": row[4], "owner_id": row[5],
            "image": row[6], "deposit": row[7]
        })
    cur.close()
    return jsonify(products)

# REQUEST PRODUCT
@app.route('/request-product', methods=['POST'])
def request_product():
    data = request.json
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO requests (buyer_id, product_id) VALUES (%s, %s)",
        (data['buyer_id'], data['product_id'])
    )
    mysql.connection.commit()
    cur.close()
    return jsonify({"message": "Request sent successfully"})

# SERVE IMAGES
@app.route('/uploads/<filename>')
def get_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Vercel needs the app object to be available at the top level
# This block only runs when you run locally
if __name__ == '__main__':
    app.run(debug=True)