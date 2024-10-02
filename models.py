from database import db

class Employee(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    designation = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    date_of_joining = db.Column(db.Date, nullable=False)
    attendance = db.relationship('Attendance', backref='employee', lazy=True)

class Attendance(db.Model):
    __tablename__ = 'attendance'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    present = db.Column(db.Boolean, default=False)
    date = db.Column(db.Date, nullable=False, default=db.func.current_date())
