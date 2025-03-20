from flask import Flask, render_template, request, redirect, url_for, jsonify
from dtp import db
from dtp.models import University, Faculty, Department, Class

from . import management

@management.route('/add_data')
def add_data():
    universities = University.query.all()
    faculties = Faculty.query.all()
    departments = Department.query.all()
    return render_template('core/data_add.html', universities=universities, faculties=faculties, departments=departments)

@management.route('/add_university', methods=['POST'])
def add_university():
    name = request.form['name']
    university = University(name=name)
    db.session.add(university)
    db.session.commit()
    return redirect(url_for('management.index'))

@management.route('/add_faculty', methods=['POST'])
def add_faculty():
    name = request.form['name']
    university_id = request.form['university_id']
    faculty = Faculty(name=name, university_id=university_id)
    db.session.add(faculty)
    db.session.commit()
    return redirect(url_for('management.index'))

@management.route('/add_department', methods=['POST'])
def add_department():
    name = request.form['name']
    faculty_id = request.form['faculty_id']
    department = Department(name=name, faculty_id=faculty_id)
    db.session.add(department)
    db.session.commit()
    return redirect(url_for('management.index'))

@management.route('/add_class', methods=['POST'])
def add_class():
    year = request.form['year']
    department_id = request.form['department_id']
    class_obj = Class(year=year, department_id=department_id)
    db.session.add(class_obj)
    db.session.commit()
    return redirect(url_for('management.index'))

@management.route('/get_faculties/<int:university_id>')
def get_faculties(university_id):
    faculties = Faculty.query.filter_by(university_id=university_id).all()
    return jsonify([{'id': f.id, 'name': f.name} for f in faculties])

@management.route('/get_departments/<int:faculty_id>')
def get_departments(faculty_id):
    departments = Department.query.filter_by(faculty_id=faculty_id).all()
    return jsonify([{'id': d.id, 'name': d.name} for d in departments])