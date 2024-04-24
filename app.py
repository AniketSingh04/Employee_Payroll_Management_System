from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# SQLite database configuration
DB_NAME = 'db/employees.db'
SCHEMA_FILE = 'db/schema.sql'

# Initialize database and create tables
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        with app.open_resource(SCHEMA_FILE, mode='r') as f:
            conn.cursor().executescript(f.read())
        conn.commit()

# Initialize database on app startup
init_db()

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Add employee route
@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        name = request.form['name']
        designation = request.form['designation']
        salary = float(request.form['salary'])

        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO employees (name, designation, salary) VALUES (?, ?, ?)",
                           (name, designation, salary))
            conn.commit()

        return redirect(url_for('view_employees'))

    return render_template('add_employee.html')

# View employees route
@app.route('/view_employees')
def view_employees():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employees")
        employees = cursor.fetchall()

    return render_template('view_employees.html', employees=employees)

# Calculate salary route
@app.route('/calculate_salary', methods=['GET', 'POST'])
def calculate_salary():
    if request.method == 'POST':
        employee_id = request.form['employee_id']
        hours_worked = float(request.form['hours_worked'])
        overtime_hours = float(request.form['overtime_hours'])
        deductions = float(request.form['deductions'])

        # Calculate salary based on inputs (simplified calculation)
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT salary FROM employees WHERE id=?", (employee_id,))
            result = cursor.fetchone()
            if result:
                salary = result[0]
                total_salary = salary + (hours_worked * 10) + (overtime_hours * 15) - deductions
                return render_template('calculate_salary.html', total_salary=total_salary)
            else:
                return "Employee not found!"

    return render_template('calculate_salary.html')

if __name__ == '__main__':
    app.run(debug=True)
