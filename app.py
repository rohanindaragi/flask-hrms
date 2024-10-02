from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import Employee, Attendance
from database import db
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hrms.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'supersecretkey'

# Initialize the database
db.init_app(app)
migrate = Migrate(app, db)  # For handling migrations


@app.route('/')
def home():
    employees = Employee.query.all()
    departments = db.session.query(Employee.department).distinct().all()
    attendance_records = Attendance.query.all()
    return render_template('home.html', employees=employees, departments=departments, attendance_records=attendance_records)


@app.route('/employees')
def employees():
    employees = Employee.query.all()
    return render_template('employees.html', employees=employees)


@app.route('/employee/add', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        name = request.form['name']
        designation = request.form['designation']
        department = request.form['department']
        date_of_joining_str = request.form['date_of_joining']
        try:
            date_of_joining = datetime.strptime(date_of_joining_str,'%Y-%m-%d').date()
        except ValueError:
            return "Invalid date format. Please use YYYY-MM-DD.",400

        new_employee = Employee(name=name, designation=designation, department=department, date_of_joining=date_of_joining)
        
        try:
            db.session.add(new_employee)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
            return "There was an issue adding the employee",500

        return redirect(url_for('employees'))
    
    return render_template('employee_form.html')


@app.route('/employee/<int:id>')
def employee_detail(id):
    employee = Employee.query.get_or_404(id)
    return render_template('employee_detail.html', employee=employee)


@app.route('/employee/edit/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):
    employee = Employee.query.get_or_404(id)
    if request.method == 'POST':
        employee.name = request.form['name']
        employee.designation = request.form['designation']
        employee.department = request.form['department']
        employee.date_of_joining = request.form['date_of_joining']
        
        db.session.commit()
        return redirect(url_for('employees'))
    
    return render_template('employee_form.html', employee=employee)


@app.route('/employee/delete/<int:id>', methods=['POST'])
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    return redirect(url_for('employees'))

# Api
@app.route('/api/employees', methods=['GET'])
def api_employees():
    employees = Employee.query.all()
    # Prepare the employee data in JSON format
    employee_list = [{
        'id': employee.id,
        'name': employee.name,
        'designation': employee.designation,
        'department': employee.department,
        'date_of_joining': employee.date_of_joining.strftime('%Y-%m-%d')
    } for employee in employees]

    return jsonify(employee_list)


@app.route('/employee/attendance', methods=['POST'])
def mark_attendance():
    data = request.get_json()
    employee_id = data.get('employee_id')
    present = data.get('present')
    
    if employee_id is None or present is None:
        return jsonify({"error":"invalid data"}),400
    
    employee = Employee.query.get(employee_id)
    if not employee:
        return jsonify({"error":"Employee not found"}),404
    
    attendance_record = Attendance(employee_id=employee_id, present=present)
    db.session.add(attendance_record)
    db.session.commit()
    
    # return jsonify({'employee_name': employee.name})
    return jsonify({"message":"Attendence marked successfully"}),201

@app.route('/employee/<int:id>/attendance', methods=['GET'])
def view_attendance(id):
    employee = Employee.query.get_or_404(id)
    attendance_records = Attendance.query.filter_by(employee_id=id).all()
    
    return render_template('employee_attendance.html', employee=employee, attendance_records=attendance_records)



@app.route('/report')
def report():
    departments = db.session.query(Employee.department, db.func.count(Employee.id)).group_by(Employee.department).all()
    return render_template('report.html', departments=departments)


@app.route('/report/data')
def report_data():
    departments = db.session.query(Employee.department, db.func.count(Employee.id)).group_by(Employee.department).all()
    report_data = [{'department': dept[0], 'count': dept[1]} for dept in departments]
    return jsonify(report_data)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)
