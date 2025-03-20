from datetime import datetime
from flask_login import UserMixin

from dtp import db, bcrypt, login_manager

@login_manager.user_loader
def load_user(user_id):
    return Student.query.get(int(user_id))

class Student(db.Model, UserMixin):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    student_number = db.Column(db.String(20), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    university_id = db.Column(db.Integer, db.ForeignKey('universities.id'), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculties.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    attendance_records = db.relationship('AttendanceRecord', backref='student', lazy=True)
    
    university = db.relationship('University', backref='students')
    faculty = db.relationship('Faculty', backref='students')
    department = db.relationship('Department', backref='students')
    class_relation = db.relationship('Class', backref='students')
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
        
    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password)
        
    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def get_available_courses(self):
        """Öğrencinin bölüm ve sınıfına göre alması gereken dersleri döndürür"""
        from dtp.models.course import Course
        return Course.query.filter_by(class_id=self.class_id).all()
    
    def get_absence_count(self, course_id):
        """Belirli bir ders için devamsızlık sayısını döndürür"""
        from models.attendance import AttendanceRecord
        return AttendanceRecord.query.filter_by(
            student_id=self.id,
            course_id=course_id
        ).count()
    
    def __repr__(self):
        return f'<Student {self.student_number} - {self.first_name} {self.last_name}>'