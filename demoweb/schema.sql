-- Database Schema for Pizza Shop

-- Create categories table
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

-- Create pizza table with foreign key to categories
CREATE TABLE pizza (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    image TEXT,
    stock INTEGER NOT NULL DEFAULT 0,
    category_id INTEGER NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- Insert sample categories
INSERT INTO categories (name) VALUES ('Classic');
INSERT INTO categories (name) VALUES ('Special');
INSERT INTO categories (name) VALUES ('Vegetarian');

-- Insert sample pizzas
INSERT INTO pizza (name, price, image, stock, category_id) VALUES 
('Margherita', 150, 'https://via.placeholder.com/150?text=Margherita', 10, 1),
('Pepperoni', 180, 'https://via.placeholder.com/150?text=Pepperoni', 8, 1),
('Hawaiian', 160, 'https://via.placeholder.com/150?text=Hawaiian', 5, 1),
('BBQ Chicken', 200, 'https://via.placeholder.com/150?text=BBQ+Chicken', 6, 2),
('Meat Lovers', 220, 'https://via.placeholder.com/150?text=Meat+Lovers', 7, 2),
('Veggie Supreme', 170, 'https://via.placeholder.com/150?text=Veggie', 4, 3);