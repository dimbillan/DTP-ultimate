# Unattendence Tracker

This project is a Flask-based attendance tracking website. It allows users to easily manage attendance records.

## Features to be added in future versions
- User-friendly interface
- Add and view attendance records
- User authentication
- Reporting and statistical analysis
- Simple and fast usage

## Installation
1. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Create the database:
   ```sh
   flask --app dtp db init
   ```
   ```sh
   flask --app dtp db migrate
   ```
   ```sh
   flask --app dtp db upgrade
   ```
3. Run the application:
   ```sh
   python run.py
   ```

## Usage
- Create a new user account or log in to an existing one.
- Add and manage attendance data.
- Review reports to analyze attendance trends.

## Technologies
This project utilizes the following technologies:
- Python & Flask
- SQLite/PostgreSQL
- HTML, CSS, JavaScript

## License
This project is licensed under the MIT License.

