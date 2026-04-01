# 🌾 Farm Management System — Project Documentation

A Django-based web application designed to streamline farm operations and data management, helping farmers keep track of daily activities, finances, livestock, and crop production.

---

## 📋 Table of Contents

- [Tech Stack](#tech-stack)
- [Features](#features)
- [Project Structure](#project-structure)
- [Database Models](#database-models)
- [Setup & Installation](#setup--installation)
- [Running the Project](#running-the-project)
- [Default URLs](#default-urls)
- [Usage Guide](#usage-guide)

---

## 🛠️ Tech Stack

| Technology     | Version / Details                  |
|----------------|------------------------------------|
| **Framework**  | Django 5.0                         |
| **Language**   | Python 3.x                        |
| **Database**   | SQLite (db.sqlite3)                |
| **Server**     | Django Development Server / Gunicorn |
| **Static Files** | WhiteNoise middleware            |
| **Frontend**   | Django Templates (HTML/CSS/JS)     |

---

## ✨ Features

### 1. 🔐 Authentication
- User **Registration** and **Login/Logout**
- Session-based authentication
- Per-user data isolation (each user sees only their own data)

### 2. 🌾 Crop Management
- Add and track crops with field details, variety, and planting/harvesting dates
- **Crop Operations** — Record operation date, name, and notes
- **Crop Expenses** — Track expense type, amount, budget, supplier, payment method, receipt number
- **Crop Sales** — Record sales with quantity, unit price, buyer info, payment status, invoice number
- Auto-calculation of total sale price (quantity × unit price)

### 3. 👨‍🌾 Employee Management
- Maintain employee records: name, phone, position, salary, performance rating

### 4. 🐄 Livestock Management
- Track animals by tag number, type, age, and breed
- **Livestock Production** — Record production date, amount, feed consumed, and comments

### 5. 🚜 Machinery Management
- Register equipment with number plate, name, purchase price, and date
- **Machinery Activities** — Log activity date, type, cost, and description
- **Machinery Maintenance** — Track maintenance dates, parts, technician, and cost

### 6. 🥛 Milk Production
- Daily milk production tracking (morning, midday, evening)
- Feed consumption tracking (morning, evening)
- Auto-calculation of total production and total consumption
- Graphical visualization of production trends

### 7. 🥚 Egg Production
- Daily egg collection tracking (morning, midday, evening)
- Feed tracking (morning, evening)
- Auto-calculation of totals

---

## 📁 Project Structure

```
Farm_Management_System/
│
├── manage.py                    # Django management script
├── db.sqlite3                   # SQLite database file
├── requirements.txt             # Python dependencies
├── procfile                     # Deployment config (Gunicorn)
├── project.md                   # This documentation file
├── README.md                    # Original README
├── MIT_license                  # License file
│
├── FarmManagementSystem/        # Django project settings
│   ├── __init__.py
│   ├── settings.py              # Project configuration
│   ├── urls.py                  # Root URL routing
│   ├── wsgi.py                  # WSGI entry point
│   └── asgi.py                  # ASGI entry point
│
├── authentication/              # Authentication app
│   ├── models.py                # (Uses Django's built-in User model)
│   ├── views.py                 # Login, Register, Logout views
│   ├── urls.py                  # Auth URL routes
│   └── templates/               # Login & Register HTML templates
│
├── homepage/                    # Main application app
│   ├── models.py                # All farm data models
│   ├── views.py                 # All farm feature views
│   ├── urls.py                  # Feature URL routes
│   ├── crops_form.py            # Crop-related forms
│   ├── employees_form.py        # Employee forms
│   ├── livestock_form.py        # Livestock forms
│   ├── machinery_form.py        # Machinery forms
│   └── templates/               # Feature HTML templates
│
├── static/                      # Static assets (CSS, JS, images)
├── staticfiles/                 # Collected static files (production)
└── venv/                        # Python virtual environment
```

---

## 🗄️ Database Models

| Model                    | Key Fields                                                             |
|--------------------------|------------------------------------------------------------------------|
| **Employees**            | Eid, Name, Country_code, Phone_number, Position, Salary, Performance   |
| **Crops**                | Cid, Field_name, Crop_name, Variety, Planting_date, Harvesting_date    |
| **Crop_expenses**        | Expense_date, Expense_type, Budget, Expense_amount, Supplier, Receipt  |
| **Crop_sales**           | Sale_date, Quantity_sold, Unit_price, Total_price, Payment_status      |
| **Crop_operations**      | Operation_date, Operation_name, Additional_notes                       |
| **Machinery**            | Number_plate, Equipment_name, Purchase_price, Purchase_date            |
| **Machinery_activities** | Activity_date, Activity_type, Activity_cost, Description               |
| **Machinery_maintenance**| Date, Machinery_part, Technician_details, Cost                         |
| **Livestock**            | Tag_number, Animal_type, Age, Breed                                    |
| **Livestock_production** | Production_date, Production_amount, Feed_consumed, Comments            |
| **Milk_production**      | Year, Month, Day, Morning/Midday/Evening production & consumption      |
| **Eggs_production**      | Year, Month, Day, Morning/Midday/Evening egg collection & feeds        |

All user-facing models include a `ForeignKey` to Django's **User** model for per-user data isolation.

---

## 🚀 Setup & Installation

### Prerequisites
- **Python 3.10+** installed and available in PATH
- **pip** (Python package manager)

### Step-by-Step Setup

#### Step 1: Open PowerShell and Navigate to the Project

```powershell
D:
cd "D:\FARMER MANAGEMENT SYSTEM\My-Farm-Project\Farm_Management_System"
```

#### Step 2: Create a Virtual Environment (Optional but Recommended)

```powershell
python -m venv venv
```

#### Step 3: Activate the Virtual Environment

```powershell
venv\Scripts\activate
```

You should see `(venv)` appear at the beginning of your terminal prompt.

#### Step 4: Install Dependencies

```powershell
pip install -r requirements.txt
```

Additionally, install `whitenoise` (used for static file serving):

```powershell
pip install whitenoise
```

#### Step 5: Run Database Migrations

```powershell
python manage.py migrate
```

This creates all required database tables in `db.sqlite3`.

#### Step 6: Create a Superuser (Admin Account)

```powershell
python manage.py createsuperuser
```

Follow the prompts to set a username, email, and password.

---

## ▶️ Running the Project

### Start the Development Server

```powershell
python manage.py runserver
```

You should see output like:

```
Watching for file changes with StatReloader
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### Stop the Server

Press `Ctrl + C` in the terminal.

---

## 🌐 Default URLs

| URL                              | Description                          |
|----------------------------------|--------------------------------------|
| `http://127.0.0.1:8000/`        | Login Page (Home)                    |
| `http://127.0.0.1:8000/register/`| User Registration Page              |
| `http://127.0.0.1:8000/admin/`  | Django Admin Panel                   |

---

## 📖 Usage Guide

1. **Register** — Go to `/register/` and create a new account
2. **Login** — Use your credentials at the home page (`/`)
3. **Dashboard** — After login, access all farm management features:
   - Add/view **Crops** and track their operations, expenses, and sales
   - Manage **Employees** with salary and performance details
   - Track **Livestock** and their production records
   - Log **Machinery** details with activities and maintenance
   - Record daily **Milk Production** and **Egg Production**
4. **Admin Panel** — Access `/admin/` with superuser credentials to manage all data directly
5. **Logout** — Use the logout option to end your session

---

## ⚠️ Notes

- The project uses **SQLite** — no external database setup required
- `DEBUG = True` is set in `settings.py` — suitable for development only
- For production deployment, update `SECRET_KEY`, set `DEBUG = False`, and configure `ALLOWED_HOSTS`
- The `whitenoise` middleware handles static files; ensure it's installed before running

---

> **Happy Farming! 🌱**
