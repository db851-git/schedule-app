# Zenith | Modern SaaS Task & Schedule Management

<img width="1440" height="677" alt="Screenshot 2026-02-26 at 9 32 58 am" src="https://github.com/user-attachments/assets/ede2395e-6bd4-4936-b264-93ea8c785e47" />


**Live Application:** https://schedule-app-deb.onrender.com

Zenith is a production-ready, full-stack schedule management application designed with a focus on clean architecture, minimal UX, and SaaS scalability. Built with Python and Flask, it features secure user authentication, dynamic daily productivity tracking, and strict relational data modeling.

## 🚀 Key Features

* **Secure Authentication:** End-to-end user registration and login system utilizing Werkzeug password hashing and secure session management.
* **Dynamic Task Management:** Create, toggle, and manage tasks with auto-sorting by time and grouping by date.
* **Daily Productivity Engine:** Calculates daily completion percentages in real-time to drive user engagement.
* **SaaS Feature Flagging:** Built-in service layer logic to enforce free-tier usage limits and restrict daily task creation.
* **Color-Coded UX:** Automated visual categorization for Priority (High/Medium/Low) and Task Type (Work/Study/Personal).

## 🏗️ Architecture & Tech Stack

This project strictly adheres to the **Separation of Concerns (SoC)** and **MVC (Model-View-Controller)** principles, decoupling routing, business logic, and database operations.

* **Backend:** Python, Flask, Flask-SQLAlchemy, Flask-WTF
* **Database:** PostgreSQL (Production) / SQLite (Development)
* **Frontend:** HTML5, Jinja2, Tailwind CSS, Feather Icons
* **Cloud Infrastructure:** Render (Compute), Neon.tech (Serverless DB), UptimeRobot (Automated Polling)

### Folder Structure
```text
├── app/
│   ├── models.py          # Relational database schemas (Users, Tasks)
│   ├── routes/            # Controllers for Authentication, Main App, and APIs
│   ├── services/          # Decoupled business logic and SaaS constraints
│   ├── templates/         # Jinja2 views (Tailwind CSS)
├── config.py              # Environment-specific configuration classes
├── run.py                 # WSGI application entry point
