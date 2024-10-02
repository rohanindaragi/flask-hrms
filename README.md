# HRMS (Human Resource Management System)

A simple and efficient Human Resource Management System (HRMS) built using Flask. This project allows organizations to manage employee data, track attendance, and generate reports.

## 🚀 Features
- **Employee Management**: Add, edit, and view employee details.
- **Attendance Tracking**: Mark attendance for employees and track their daily presence.
- **Basic Reporting**: View reports on employee statistics, such as employee count by department.
- **RESTful API**: Provides an API to access employee data in JSON format.
- **Responsive Design**: Clean and modern UI using Bootstrap for a seamless experience on any device.

## 📷 Screenshots
### Home Page
![home](https://github.com/user-attachments/assets/05438a41-dd3f-4dc0-aed4-efb03f3d447d)


### Add Employee
![addemp](https://github.com/user-attachments/assets/45bb73bf-ba4c-4dba-bbae-9e67d4a816ee)

### Employees details
![empDet](https://github.com/user-attachments/assets/6e4455c3-e95a-4f46-8097-7f4e24abca98)



## 💻 Technologies Used
- **Backend**: Flask, Python
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML, CSS (Bootstrap), JavaScript
- **API**: RESTful API with Flask
- **Version Control**: Git, GitHub

## ⚙️ Installation and Setup
Follow these steps to run the project locally:

1. Clone the repository:
   ```bash
   git clone https://github.com/rohanindaragi/flask-hrms.git
   cd flask-hrms
2. Create and activate a virtual environment:
   # For Windows
        python -m venv venv
        venv\Scripts\activate

   # For Mac/Linux
        python3 -m venv venv
        source venv/bin/activate
   
3. Install the required packages:
   pip install -r requirements.txt
   
4. Set up the database:
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade

5. Run the application:
   flask run

6. Open your browser and navigate to:
   http://127.0.0.1:5000/

📄 API Endpoints
  Get All Employees
  Endpoint: /api/employees
  Method: GET
  Response:
  [
  {
    "id": 1,
    "name": "John Doe",
    "designation": "Software Engineer",
    "department": "Engineering",
    "date_of_joining": "2023-01-10"
  }
]

Mark Attendance:
    Endpoint: /employee/attendance
    Method: POST

Payload:
    {
      "employee_id": 1,
      "present": true
    }

📊 Future Enhancements
    Implement advanced reporting features.
    Add support for employee roles and permissions.
    Integrate with a notification system for reminders.
    🛠 Known Issues
    The application currently uses SQLite for simplicity. For production, a more robust database like PostgreSQL is recommended.
    Attendance reporting is currently limited to daily records.
    
🤝 Contributing
    Contributions are welcome! If you'd like to contribute, please fork the repository and submit a pull request.

📄 License
    This project is licensed under the MIT License - see the LICENSE file for details.

🙌 Acknowledgements
    Flask
    Bootstrap


   


