import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('inventory.db')
cursor = conn.cursor()

# Create tblLocations
cursor.execute('''
CREATE TABLE IF NOT EXISTS tblLocations (
    LocationID INTEGER PRIMARY KEY AUTOINCREMENT,
    MainLocation TEXT NOT NULL,
    Sublocation TEXT
)
''')

# Create tblCategories
cursor.execute('''
CREATE TABLE IF NOT EXISTS tblCategories (
    CategoryID INTEGER PRIMARY KEY AUTOINCREMENT,
    CategoryName TEXT NOT NULL
)
''')

# Create tblMain
cursor.execute('''
CREATE TABLE IF NOT EXISTS tblMain (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    LocationID INTEGER,
    CategoryID INTEGER,
    Description TEXT NOT NULL,
    Notes TEXT,
    ParentID INTEGER,
    FOREIGN KEY (LocationID) REFERENCES tblLocations (LocationID),
    FOREIGN KEY (CategoryID) REFERENCES tblCategories (CategoryID),
    FOREIGN KEY (ParentID) REFERENCES tblMain (ID)
)
''')

# Create tblDetail
cursor.execute('''
CREATE TABLE IF NOT EXISTS tblDetail (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    tblMainID INTEGER,
    Make TEXT,
    Model TEXT,
    SN TEXT,
    Cost REAL,
    Quantity INTEGER,
    Condition TEXT,
    PurchaseDate DATE,
    Notes TEXT,
    FOREIGN KEY (tblMainID) REFERENCES tblMain (ID)
)
''')

# Commit changes and close connection
conn.commit()
conn.close()

print("Database and tables created successfully.")