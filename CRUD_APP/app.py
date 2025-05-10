import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="NorthStar101!",
    database="crud_app"
)

cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    age INT
)
""")

print("Table 'users' created or already exists.")
