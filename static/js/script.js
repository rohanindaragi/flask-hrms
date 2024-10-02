/* File: static/js/script.js */

// Simple form validation for employee creation
function validateEmployeeForm() {
    const name = document.getElementById('name').value;
    const designation = document.getElementById('designation').value;
    const department = document.getElementById('department').value;

    if (name === "" || designation === "" || department === "") {
        alert("All fields are required!");
        return false;
    }
    return true;
}

// Example for dynamically loading employee list
function loadEmployees() {
    fetch('/employees')
        .then(response => response.json())
        .then(data => {
            const employeeList = document.getElementById('employee-list');
            employeeList.innerHTML = '';
            data.forEach(employee => {
                const li = document.createElement('li');
                li.textContent = `${employee.name} - ${employee.designation}`;
                employeeList.appendChild(li);
            });
        })
        .catch(error => console.error('Error fetching employees:', error));
}

// Marking attendance with confirmation popup
function confirmAttendance(employeeId) {
    const present = confirm("Mark this employee as present?");
    fetch(`/employee/attendance`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ employee_id: employeeId, present: present })
    })
    .then(response => response.json())
    .then(data => {
        alert(`Attendance marked for ${data.employee_name}`);
    })
    .catch(error => console.error('Error marking attendance:', error));
}

// Dynamic chart rendering using Chart.js
function renderDepartmentChart(departmentData) {
    const ctx = document.getElementById('departmentChart').getContext('2d');
    const labels = departmentData.map(item => item.department);
    const counts = departmentData.map(item => item.count);

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Number of Employees',
                data: counts,
                backgroundColor: 'rgba(54, 162, 235, 0.6)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}

// Fetching department report data and rendering chart
function loadDepartmentReport() {
    fetch('/report/data')
        .then(response => response.json())
        .then(data => {
            renderDepartmentChart(data);
        })
        .catch(error => console.error('Error loading report data:', error));
}

// Call functions on page load
document.addEventListener('DOMContentLoaded', () => {
    const employeeForm = document.getElementById('employee-form');
    if (employeeForm) {
        employeeForm.onsubmit = validateEmployeeForm;
    }

    // Load the employee list if the element exists
    const employeeList = document.getElementById('employee-list');
    if (employeeList) {
        loadEmployees();
    }

    // Load the department report if on the report page
    const departmentChart = document.getElementById('departmentChart');
    if (departmentChart) {
        loadDepartmentReport();
    }
});
