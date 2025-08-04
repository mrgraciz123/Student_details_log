from flask import Flask, request, render_template
import mysql.connector
from mysql.connector import errorcode

app = Flask(__name__)

# MySQL connection setup
db_config = {
    'host': "localhost",
    'user': "root",
    'password': "226028"
}

# Step 1: Connect to MySQL without specifying the database
db = mysql.connector.connect(**db_config)
cursor = db.cursor()

# Step 2: Create database if it doesn't exist
try:
    cursor.execute("CREATE DATABASE IF NOT EXISTS studentdb")
    print("✅ Database 'studentdb' ensured.")
except mysql.connector.Error as err:
    print(f"⚠️ Error creating database: {err}")

# Step 3: Connect to 'studentdb'
db_config['database'] = 'studentdb'
db = mysql.connector.connect(**db_config)
cursor = db.cursor()

# Step 4: Create table if it doesn't exist
table_query = """
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    roll INT,
    email VARCHAR(100),
    branch VARCHAR(100)
);
"""
try:
    cursor.execute(table_query)
    print("✅ Table 'students' ensured.")
except mysql.connector.Error as err:
    print(f"⚠️ Error creating table: {err}")

@app.route('/')
def home():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    roll = request.form['roll']
    email = request.form['email']
    branch = request.form['branch']

    query = "INSERT INTO students (name, roll, email, branch) VALUES (%s, %s, %s, %s)"
    values = (name, roll, email, branch)
    cursor.execute(query, values)
    db.commit()
    return render_template('success.html', name=name, roll=roll, email=email, branch=branch)


if __name__ == '__main__':
    app.run(debug=True)