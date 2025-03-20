from datetime import datetime
from dtp import db

class AttendanceRecord(db.Model):
    __tablename__ = 'attendance_records'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, student_id, course_id, date=None):
        self.student_id = student_id
        self.course_id = course_id
        self.date = date or datetime.utcnow().date()
    
    @classmethod
    def add_absence(cls, student_id, course_id, date=None):
        """Öğrenci için yeni bir devamsızlık kaydı ekler"""
        absence = cls(student_id=student_id, course_id=course_id, date=date)
        db.session.add(absence)
        db.session.commit()
        return absence
    
    @classmethod
    def remove_absence(cls, absence_id):
        """Belirli bir devamsızlık kaydını siler"""
        absence = cls.query.get(absence_id)
        if absence:
            db.session.delete(absence)
            db.session.commit()
            return True
        return False
    
    def __repr__(self):
        return f'<AttendanceRecord {self.student.student_number} - {self.course.code} - {self.date}>'