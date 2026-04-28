# filepath: app.py
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# กำหนดโฟลเดอร์ static
app.static_folder = 'static'
app.static_url_path = '/static'

# Database file
DB_NAME = '/home/punyawat007/demoweb/demoweb/pizza.db'


def get_db_connection():
    """เชื่อมต่อฐานข้อมูล"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """สร้างตารางและข้อมูลเริ่มต้น"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # สร้างตาราง categories
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    
    # สร้างตาราง pizza
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pizza (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            image TEXT,
            stock INTEGER NOT NULL DEFAULT 0,
            category_id INTEGER NOT NULL,
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )
    ''')
    
    # เพิ่มข้อมูลตัวอย่างถ้าว่าง
    cursor.execute('SELECT COUNT(*) FROM categories')
    if cursor.fetchone()[0] == 0:
        # เพิ่มหมวดหมู่
        categories = [('Classic',), ('Special',), ('Vegetarian',)]
        cursor.executemany('INSERT INTO categories (name) VALUES (?)', categories)
        
        # เพิ่มพิซซาตัวอย่าง
        pizzas = [
            ('Margherita', 150, '/static/images/pizza1.jpg', 10, 1),
            ('Pepperoni', 180, '/static/images/pizza2.jpg', 8, 1),
            ('Hawaiian', 160, '/static/images/pizza3.jpg', 5, 1),
            ('BBQ Chicken', 200, '/static/images/pizza4.jpg', 6, 2),
            ('Meat Lovers', 220, '/static/images/pizza5.jpg', 7, 2),
            ('Veggie Supreme', 170, '/static/images/pizza6.jpg', 4, 3),
        ]
        cursor.executemany(
            'INSERT INTO pizza (name, price, image, stock, category_id) VALUES (?, ?, ?, ?, ?)',
            pizzas
        )
    
    conn.commit()
    conn.close()


# ==================== Routes ====================

@app.route('/')
def index():
    """หน้าแรก - แสดงรายการพิซซาทั้งหมด (JOIN category)"""
    conn = get_db_connection()
    # JOIN เพื่อดึงชื่อหมวดหมู่มาด้วย
    pizzas = conn.execute('''
        SELECT pizza.*, categories.name as category_name
        FROM pizza
        JOIN categories ON pizza.category_id = categories.id
    ''').fetchall()
    conn.close()
    return render_template('pizzamenu.html', pizzas=pizzas)


@app.route('/add', methods=['GET', 'POST'])
def add_pizza():
    """หน้าเพิ่มสินค้า"""
    conn = get_db_connection()
    categories = conn.execute('SELECT * FROM categories').fetchall()
    
    if request.method == 'POST':
        # รับข้อมูลจากฟอร์ม
        name = request.form['name']
        price = float(request.form['price'])
        image = request.form['image']
        stock = int(request.form['stock'])
        category_id = int(request.form['category_id'])
        
        # เพิ่มข้อมูลลงฐานข้อมูล
        conn.execute('''
            INSERT INTO pizza (name, price, image, stock, category_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, price, image, stock, category_id))
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))
    
    conn.close()
    return render_template('append.html', categories=categories)


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_pizza(id):
    """หน้าแก้ไขสินค้า"""
    conn = get_db_connection()
    categories = conn.execute('SELECT * FROM categories').fetchall()
    
    if request.method == 'POST':
        # อัปเดตข้อมูล
        name = request.form['name']
        price = float(request.form['price'])
        image = request.form['image']
        stock = int(request.form['stock'])
        category_id = int(request.form['category_id'])
        
        conn.execute('''
            UPDATE pizza
            SET name = ?, price = ?, image = ?, stock = ?, category_id = ?
            WHERE id = ?
        ''', (name, price, image, stock, category_id, id))
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))
    
    # ดึงข้อมูลพิซซาที่ต้องการแก้ไข
    pizza = conn.execute('SELECT * FROM pizza WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    return render_template('edit.html', pizza=pizza, categories=categories)


@app.route('/delete/<int:id>')
def delete_pizza(id):
    """ลบสินค้า"""
    conn = get_db_connection()
    conn.execute('DELETE FROM pizza WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))


# ==================== Main ====================
if __name__ == '__main__':
    # สร้างฐานข้อมูลก่อนรัน
    init_db()
    app.run(debug=True)
