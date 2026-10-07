# Django Student Management System

A web-based Student Management System developed with **Python and Django** for educational and academic management purposes.

This project is based on the original Django Student Management System by **Vijay Thapa / SuperCoders** and has been customized and extended with additional features for practical use.

## Features

### A. HOD / Admin

* Admin/HOD Dashboard
* Manage Students
* Add, Update and Delete Students
* Manage Staff/Teachers
* Manage Courses
* Manage Subjects
* Manage Academic Sessions
* View Student Attendance
* Manage Student Results
* Manage Student Leave
* Manage Student/Staff Feedback
* Search and filter records
* Student registration system
* Student profile management

### B. Student Management

* Student profiles
* Course assignment
* Academic session assignment
* Student registration
* Student attendance
* Student results
* Student leave requests
* Student feedback
* Student dashboard

### C. Teacher / Staff Management

* Teacher profiles
* Subject assignment
* Student attendance
* Student results
* Leave requests
* Feedback to HOD

## Fee Management

The project includes a monthly student fee management system.

### HOD / Admin Fee Features

* Manage student fees
* Monthly fee records
* Fee period/month
* Total fee
* Paid fee
* Remaining fee calculation
* Paid, Partial and Unpaid status
* Due date
* Paid date
* Add new monthly fee without overwriting previous records
* Edit individual fee records
* View complete fee history for each student
* Manage Fee shows the latest fee for each student
* Fee History keeps all previous monthly records
* Course filtering
* Fee searching

### Example

A student can have separate monthly records:

* October 2026 — Rs. 5,000 — Paid
* November 2026 — Rs. 5,000 — Paid
* December 2026 — Rs. 5,000 — Partial
* January 2027 — Rs. 5,000 — Unpaid

Previous monthly records are preserved in Fee History.

## Technology

* **Python**
* **Django**
* **SQLite**
* **HTML**
* **CSS**
* **JavaScript**
* **Bootstrap**
* **AdminLTE**

## Project Structure

```text
django-student-management-system/
│
├── manage.py
├── requirements.txt
├── db.sqlite3
│
├── student_management_app/
│   ├── models.py
│   ├── HodViews.py
│   ├── StaffViews.py
│   ├── StudentViews.py
│   ├── urls.py
│   └── templates/
│
└── student_management_system/
    ├── settings.py
    ├── urls.py
    └── ...
```

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/rashidhussain110/BigDreams.git
```

Enter the project:

```bash
cd BigDreams
```

### 2. Create a Virtual Environment

For Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Run Database Migrations

```bash
python manage.py migrate
```

### 5. Create an Admin/HOD Account

```bash
python manage.py createsuperuser
```

Follow the instructions in the terminal.

### 6. Start the Development Server

```bash
python manage.py runserver
```

Open the project in your browser:

```text
http://127.0.0.1:8000/
```

## Development Status

This project is under active development.

Features are being added and improved gradually, including:

* Student management
* Academic management
* Monthly fee management
* Fee history
* Student registration
* Attendance
* Results
* Leave management
* Feedback management

## Original Project

This project was originally based on the **Django Student Management System** developed by **Vijay Thapa / SuperCoders**.

The original project was created as part of learning Django and has been customized and extended for this project.

Original repository:

https://github.com/vijaythapa333/django-student-management-system

## License

This project is intended for educational and development purposes.

Please review the original project's license and attribution requirements before redistributing or publishing modified versions.
