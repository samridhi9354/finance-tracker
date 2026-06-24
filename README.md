# Personal Finance Tracker
Personal Finance Tracker built with Django

A full-stack personal finance management application built with Django that helps users track income, expenses, and spending patterns through an intuitive dashboard and visual analytics.

## Overview

Personal Finance Tracker enables users to manage daily financial transactions, categorize expenses, monitor cash flow, and gain insights into spending habits through interactive charts and reports.

The application features secure authentication, personalized transaction management, category-based expense tracking, and a responsive user interface with dark/light mode support.

## Features

### Authentication & Security

* User registration and login system
* Secure session-based authentication
* User-specific financial data isolation

### Transaction Management

* Add income and expense records
* Edit and delete transactions
* Transaction history tracking
* Search and filter transactions

### Financial Dashboard

* Total income overview
* Total expense summary
* Current balance calculation
* Recent transaction activity

### Data Visualization

* Interactive expense distribution charts
* Category-wise spending analysis
* Visual financial insights using Chart.js

### Category Management

* Custom expense categories
* User-specific category organization
* Default categories on account creation

### User Experience

* Responsive design for desktop and mobile devices
* Dark/Light mode support
* Clean and modern user interface

## Tech Stack

| Category       | Technology                   |
| -------------- | ---------------------------- |
| Backend        | Django 5, Python             |
| Database       | SQLite                       |
| Frontend       | HTML, CSS, Django Templates  |
| Styling        | Tailwind CSS                 |
| Charts         | Chart.js                     |
| Authentication | Django Authentication System |
| Deployment     | Gunicorn, WhiteNoise         |

## Screenshots

Add screenshots of:

* Dashboard
* Transaction Management
* Expense Analytics
* Dark Mode Interface

## Architecture

```text
User
 │
 ▼
Django Templates
 │
 ▼
Django Views
 │
 ▼
Models (Transaction, Category)
 │
 ▼
SQLite Database
```

## Installation

### Clone the Repository

```bash
git clone https://github.com/your-username/finance-tracker.git
cd finance-tracker
```

### Create a Virtual Environment

```bash
python -m venv venv
```

### Activate the Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Migrations

```bash
python manage.py migrate
```

### Start the Development Server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## Learning Outcomes

* Django MVT Architecture
* Database Design using ORM
* Authentication and Authorization
* CRUD Operations
* Data Visualization
* Responsive UI Development
* Deployment Workflow

## Future Enhancements

* Budget planning and tracking
* Recurring transactions
* Export reports (PDF/Excel)
* REST API support
* PostgreSQL integration
* Financial goal tracking

## Author

Samridhi Shrivastava

