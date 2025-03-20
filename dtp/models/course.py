from dtp import db

class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    attendance_records = db.relationship('AttendanceRecord', backref='course', lazy=True)
    
    def __repr__(self):
        return f'<Course {self.code} - {self.name}>'