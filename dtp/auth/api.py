from flask import jsonify

from dtp.models import Class, Department, Faculty

from . import auth

@auth.route("/api/faculties/<int:university_id>", methods=["GET"])
def get_faculties(university_id):
    faculties = Faculty.query.filter_by(university_id=university_id).all()
    return jsonify([{"id": f.id, "name": f.name} for f in faculties])


@auth.route("/api/departments/<int:faculty_id>", methods=["GET"])
def get_departments(faculty_id):
    departments = Department.query.filter_by(faculty_id=faculty_id).all()
    return jsonify([{"id": d.id, "name": d.name} for d in departments]) 

@auth.route("/api/classes/<int:department_id>", methods=["GET"])
def get_classes(department_id):
    classes = Class.query.filter_by(department_id=department_id).all()
    return jsonify([{"id": c.id, "year": c.year} for c in classes])