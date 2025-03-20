from datetime import datetime
from dtp import db

class University(db.Model):
    __tablename__ = 'universities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    faculties = db.relationship('Faculty', backref='university', lazy=True)
    
    def __repr__(self):
        return f'<University {self.name}>'

class Faculty(db.Model):
    __tablename__ = 'faculties'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    university_id = db.Column(db.Integer, db.ForeignKey('universities.id'), nullable=False)
    departments = db.relationship('Department', backref='faculty', lazy=True)
    
    def __repr__(self):
        return f'<Faculty {self.name}>'

class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculties.id'), nullable=False)
    classes = db.relationship('Class', backref='department', lazy=True)
    
    def __repr__(self):
        return f'<Department {self.name}>'

class Class(db.Model):
    __tablename__ = 'classes'
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)  # 1, 2, 3, 4 (sınıf)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    courses = db.relationship('Course', backref='class', lazy=True)
    
    def __repr__(self):
        return f'<Class {self.year}>'