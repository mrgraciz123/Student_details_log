from flask import Flask, request, render_template
import mysql.connector

app = Flask(__name__)

# Database connection details
db_info = {
    'host': 'localhost',
    'user': 'root',
    'password': '226028'
}

# Connect to MySQL server (no DB yet)
conn = mysql.connector.connect(**db_info)
cursor = conn.cursor()

# Create the database if it doesn't exist
cursor.execute("CREATE DATABASE IF NOT EXISTS studentdb")
print("✅ Database is ready.")

# Connect again, this time to 'studentdb'
db_info['database'] = 'studentdb'
conn = mysql.connector.connect(**db_info)
cursor = conn.cursor()

# Create the table if not already created
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    roll INT,
    email VARCHAR(100),
    branch VARCHAR(100)
)
""")
print("✅ Table is ready.")

# Home page with form
@app.route('/')
def home():
    return render_template('form.html')

# Form submission route
@app.route('/submit', methods=['POST'])
def submit():
    # Get data from form
    name = request.form['name']
    roll = request.form['roll']
    email = request.form['email']
    branch = request.form['branch']

    # Save data to the database
    query = "INSERT INTO students (name, roll, email, branch) VALUES (%s, %s, %s, %s)"
    values = (name, roll, email, branch)
    cursor.execute(query, values)
    conn.commit()

    return render_template('success.html', name=name, roll=roll, email=email, branch=branch)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
