from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from models import Employee, Attendance
from database import db

main_routes = Blueprint('main_routes', __name__)

@main_routes.route('/')
def home():
    employees = Employee.query.all()
    departments = db.session.query(Employee.department).distinct().all()
    attendance_records = Attendance.query.all()
    return render_template('home.html', employees=employees, departments=departments, attendance_records=attendance_records)

@main_routes.route('/employees')
def employees():
    employees = Employee.query.all()
    return render_template('employees.html', employees=employees)

@main_routes.route('/employee/add', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        name = request.form['name']
        designation = request.form['designation']
        department = request.form['department']
        date_of_joining = request.form['date_of_joining']

        new_employee = Employee(name=name, designation=designation, department=department, date_of_joining=date_of_joining)
        db.session.add(new_employee)
        db.session.commit()

        return redirect(url_for('main_routes.employees'))
    
    return render_template('employee_form.html')

@main_routes.route('/employee/<int:id>')
def employee_detail(id):
    employee = Employee.query.get_or_404(id)
    return render_template('employee_detail.html', employee=employee)

@main_routes.route('/employee/edit/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):
    employee = Employee.query.get_or_404(id)
    if request.method == 'POST':
        employee.name = request.form['name']
        employee.designation = request.form['designation']
        employee.department = request.form['department']
        employee.date_of_joining = request.form['date_of_joining']
        
        db.session.commit()
        return redirect(url_for('main_routes.employees'))
    
    return render_template('employee_form.html', employee=employee)

@main_routes.route('/employee/delete/<int:id>', methods=['POST'])
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    return redirect(url_for('main_routes.employees'))

@main_routes.route('/employee/attendance', methods=['POST'])
def mark_attendance():
    data = request.json
    employee_id = data.get('employee_id')
    present = data.get('present')
    
    attendance_record = Attendance(employee_id=employee_id, present=present)
    db.session.add(attendance_record)
    db.session.commit()
    
    employee = Employee.query.get(employee_id)
    return jsonify({'employee_name': employee.name})

@main_routes.route('/report')
def report():
    departments = db.session.query(Employee.department, db.func.count(Employee.id)).group_by(Employee.department).all()
    return render_template('report.html', departments=departments)

@main_routes.route('/report/data')
def report_data():
    departments = db.session.query(Employee.department, db.func.count(Employee.id)).group_by(Employee.department).all()
    report_data = [{'department': dept[0], 'count': dept[1]} for dept in departments]
    return jsonify(report_data)
