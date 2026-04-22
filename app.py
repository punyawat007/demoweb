import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'pizza_secret_key'


def init_db():
    """Initialize database with tables and sample data."""
    conn = sqlite3.connect('pizza.db')
    cursor = conn.cursor()

    # Create categories table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')

    # Create pizza table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pizza (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            image TEXT,
            stock INTEGER NOT NULL DEFAULT 0,
            category_id INTEGER,
            FOREIGN KEY (category_id) REFERENCES categories (id)
        )
    ''')

    # Insert sample categories if empty
    cursor.execute('SELECT COUNT(*) FROM categories')
    if cursor.fetchone()[0] == 0:
        categories = [
            ('Classic',),
            ('Premium',),
            ('Vegetarian',),
            ('Special',)
        ]
        cursor.executemany('INSERT INTO categories (name) VALUES (?)', categories)

    # Insert sample pizzas if empty
    cursor.execute('SELECT COUNT(*) FROM pizza')
    if cursor.fetchone()[0] == 0:
        pizzas = [
            ('Margherita', 199, 'https://via.placeholder.com/300x200?text=Margherita', 50, 1),
            ('Pepperoni', 249, 'https://via.placeholder.com/300x200?text=Pepperoni', 30, 1),
            ('Hawaiian', 229, 'https://via.placeholder.com/300x200?text=Hawaiian', 25, 2),
            ('BBQ Chicken', 279, 'https://via.placeholder.com/300x200?text=BBQ+Chicken', 20, 2),
            ('Veggie Supreme', 259, 'https://via.placeholder.com/300x200?text=Veggie', 15, 3),
            ('Truffle Mushroom', 329, 'https://via.placeholder.com/300x200?text=Truffle', 10, 4)
        ]
        cursor.executemany(
            'INSERT INTO pizza (name, price, image, stock, category_id) VALUES (?, ?, ?, ?, ?)',
            pizzas
        )

    conn.commit()
    conn.close()


def get_db_connection():
    """Get database connection."""
    conn = sqlite3.connect('pizza.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    """Home page - display all pizzas with category info."""
    conn = get_db_connection()
    pizzas = conn.execute('''
        SELECT pizza.*, categories.name as category_name
        FROM pizza
        LEFT JOIN categories ON pizza.category_id = categories.id
    ''').fetchall()
    conn.close()
    return render_template('index.html', pizzas=pizzas)


@app.route('/add', methods=('GET', 'POST'))
def add():
    """Add new pizza product."""
    conn = get_db_connection()
    categories = conn.execute('SELECT * FROM categories').fetchall()

    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        image = request.form['image'] or 'https://via.placeholder.com/300x200?text=Pizza'
        stock = int(request.form['stock'])
        category_id = int(request.form['category_id'])

        conn.execute(
            'INSERT INTO pizza (name, price, image, stock, category_id) VALUES (?, ?, ?, ?, ?)',
            (name, price, image, stock, category_id)
        )
        conn.commit()
        conn.close()
        flash('เพิ่มสินค้าสำเร็จ!', 'success')
        return redirect(url_for('index'))

    conn.close()
    return render_template('add.html', categories=categories)


@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit(id):
    """Edit pizza product."""
    conn = get_db_connection()
    pizza = conn.execute('SELECT * FROM pizza WHERE id = ?', (id,)).fetchone()
    categories = conn.execute('SELECT * FROM categories').fetchall()

    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        image = request.form['image'] or 'https://via.placeholder.com/300x200?text=Pizza'
        stock = int(request.form['stock'])
        category_id = int(request.form['category_id'])

        conn.execute(
            '''UPDATE pizza 
               SET name = ?, price = ?, image = ?, stock = ?, category_id = ? 
               WHERE id = ?''',
            (name, price, image, stock, category_id, id)
        )
        conn.commit()
        conn.close()
        flash('แก้ไขสินค้าสำเร็จ!', 'success')
        return redirect(url_for('index'))

    conn.close()
    return render_template('edit.html', pizza=pizza, categories=categories)


@app.route('/delete/<int:id>')
def delete(id):
    """Delete pizza product."""
    conn = get_db_connection()
    conn.execute('DELETE FROM pizza WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('ลบสินค้าสำเร็จ!', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    init_db()
    app.run(debug=True)