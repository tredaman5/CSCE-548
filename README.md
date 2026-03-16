# CSCE 548 – Workout Tracker Application

This repository contains my CSCE 548 application project. The application was built in stages across Projects 1–4 using generative AI assistance. Look at the PDF to see how to deploy this Application and see the test results.

All application code is located inside the `project-1` folder.

---

## Project Overview

This system is a Workout Tracker application built with a layered architecture:

- **Data Layer** – repository classes that interact with PostgreSQL
- **Business Layer** – service classes that validate input and call the repositories
- **Service Layer** – FastAPI REST endpoints
- **Client Layer** – a web front end hosted by the FastAPI application

The application supports working with:

- Users
- Exercises
- Workouts

---

## Repository Structure

```text
project-1/
│
├── app/
│   ├── api/              # FastAPI service layer
│   ├── services/         # business layer
│   ├── repositories/     # data access layer
│   ├── db.py             # database connection
│   └── __init__.py
│
├── web/                  # Project 3 and 4 web client
│   ├── index.html
│   ├── styles.css
│   └── app.js
│
├── client/               # console client from Project 2
│   └── console_client.py
│
├── sql/
│   ├── 01_create_tables.sql
│   └── 02_seed_data.sql
│
├── main.py
└── requirements.txt