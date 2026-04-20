import sqlite3

# Connect to SQLite database (creates the file if it doesn't exist)
conn = sqlite3.connect('flowers_store.db')
cursor = conn.cursor()

# Create Categories table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
''')

# Create Flowers table with Foreign Key
cursor.execute('''
CREATE TABLE IF NOT EXISTS Flowers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category_id INTEGER,
    price REAL,
    description TEXT,
    FOREIGN KEY (category_id) REFERENCES Categories(id)
)
''')

# Insert mock data into Categories
categories = [
    ('Seasonal',),
    ('Exotic',),
    ('Local',)
]
cursor.executemany('INSERT INTO Categories (name) VALUES (?)', categories)

# Insert mock data into Flowers
flowers = [
    ('Rose', 1, 50.0, 'Red rose'),
    ('Tulip', 1, 40.0, 'Yellow tulip'),
    ('Orchid', 2, 100.0, 'Rare orchid'),
    ('Sunflower', 3, 30.0, 'Bright sunflower'),
    ('Lily', 1, 45.0, 'White lily')
]
cursor.executemany('INSERT INTO Flowers (name, category_id, price, description) VALUES (?, ?, ?, ?)', flowers)

# Commit changes and close connection
conn.commit()
conn.close()

print("Database 'flowers_store.db' created successfully with tables and mock data!")