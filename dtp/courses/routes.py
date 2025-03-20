from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, session
from flask_login import login_required, current_user
from dtp import db
from dtp.models.university import University, Faculty, Department, Class
from dtp.models.course import Course
from dtp.courses.forms import CourseForm

from . import courses

@courses.route('/courses/add', methods=['GET', 'POST'])
def add_course():
    form = CourseForm()
    
    # Get all universities for the initial dropdown
    universities = University.query.all()
    form.university_id.choices = [(u.id, u.name) for u in universities]

    faculties = Faculty.query.filter_by(university_id=form.university_id.data).all() if form.university_id.data else []
    form.faculty_id.choices = [(f.id, f.name) for f in faculties] if faculties else []

    departments = Department.query.filter_by(faculty_id=form.faculty_id.data).all() if form.faculty_id.data else []
    form.department_id.choices = [(d.id, d.name) for d in departments] if departments else []

    classes = Class.query.filter_by(department_id=form.department_id.data).all() if form.department_id.data else []
    form.class_id.choices = [(c.id, f"Year {c.year}") for c in classes] if classes else []
    # If form is submitted and valid
    if form.validate_on_submit():
        course = Course(
            code=form.code.data,
            name=form.name.data,
            class_id=form.class_id.data
        )
        
        # Save the selections in session for future use
        session['last_university_id'] = form.university_id.data
        session['last_faculty_id'] = form.faculty_id.data
        session['last_department_id'] = form.department_id.data
        session['last_class_id'] = form.class_id.data
        
        db.session.add(course)
        try:
            db.session.commit()
            flash('Course added successfully!', 'success')
            return redirect(url_for('courses.add_course'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding course: {str(e)}', 'danger')
    
    # Load previous selections from session if available
    if request.method == 'GET':
        if 'last_university_id' in session:
            form.university_id.data = session.get('last_university_id')
            
            # Load faculties based on selected university
            faculties = Faculty.query.filter_by(university_id=form.university_id.data).all()
            form.faculty_id.choices = [(f.id, f.name) for f in faculties]
            
            if 'last_faculty_id' in session:
                form.faculty_id.data = session.get('last_faculty_id')
                
                # Load departments based on selected faculty
                departments = Department.query.filter_by(faculty_id=form.faculty_id.data).all()
                form.department_id.choices = [(d.id, d.name) for d in departments]
                
                if 'last_department_id' in session:
                    form.department_id.data = session.get('last_department_id')
                    
                    # Load classes based on selected department
                    classes = Class.query.filter_by(department_id=form.department_id.data).all()
                    form.class_id.choices = [(c.id, f"Year {c.year}") for c in classes]
                    
                    if 'last_class_id' in session:
                        form.class_id.data = session.get('last_class_id')
    
    return render_template('courses/add_course.html', form=form, title='Add Course')

@courses.route('/get_faculties/<int:university_id>')
def get_faculties(university_id):
    faculties = Faculty.query.filter_by(university_id=university_id).all()
    faculty_list = [{'id': f.id, 'name': f.name} for f in faculties]
    return jsonify({'faculties': faculty_list})

@courses.route('/get_departments/<int:faculty_id>')
def get_departments(faculty_id):
    departments = Department.query.filter_by(faculty_id=faculty_id).all()
    department_list = [{'id': d.id, 'name': d.name} for d in departments]
    return jsonify({'departments': department_list})

@courses.route('/get_classes/<int:department_id>')
def get_classes(department_id):
    classes = Class.query.filter_by(department_id=department_id).all()
    class_list = [{'id': c.id, 'name': f"Year {c.year}"} for c in classes]
    return jsonify({'classes': class_list})

@courses.route('/courses', methods=['GET'])
def list_courses():
    form = CourseForm()
    
    # Kullanıcıya üniversite, fakülte, bölüm ve sınıf seçme seçenekleri sun
    universities = University.query.all()
    form.university_id.choices = [(u.id, u.name) for u in universities]
    
    selected_university_id = request.args.get('university_id', type=int)
    faculties = Faculty.query.filter_by(university_id=selected_university_id).all() if selected_university_id else []
    form.faculty_id.choices = [(f.id, f.name) for f in faculties]
    
    selected_faculty_id = request.args.get('faculty_id', type=int)
    departments = Department.query.filter_by(faculty_id=selected_faculty_id).all() if selected_faculty_id else []
    form.department_id.choices = [(d.id, d.name) for d in departments]
    
    selected_department_id = request.args.get('department_id', type=int)
    classes = Class.query.filter_by(department_id=selected_department_id).all() if selected_department_id else []
    form.class_id.choices = [(c.id, f"Year {c.year}") for c in classes]
    
    selected_class_id = request.args.get('class_id', type=int)
    courses = Course.query.filter_by(class_id=selected_class_id).all() if selected_class_id else []
    
    return render_template('courses/courses.html', courses=courses, form=form, title='Courses')

@courses.route('/courses/<int:course_id>/edit', methods=['GET', 'POST'])
def edit_course(course_id):
    course = Course.query.get_or_404(course_id)
    
    # Get the current class, department, faculty, and university
    current_class = Class.query.get(course.class_id)
    current_department = Department.query.get(current_class.department_id)
    current_faculty = Faculty.query.get(current_department.faculty_id)
    current_university = University.query.get(current_faculty.university_id)
    
    form = CourseForm(obj=course)
    
    # Initialize all dropdowns with current values
    universities = University.query.all()
    form.university_id.choices = [(u.id, u.name) for u in universities]
    form.university_id.data = current_university.id
    
    faculties = Faculty.query.filter_by(university_id=current_university.id).all()
    form.faculty_id.choices = [(f.id, f.name) for f in faculties]
    form.faculty_id.data = current_faculty.id
    
    departments = Department.query.filter_by(faculty_id=current_faculty.id).all()
    form.department_id.choices = [(d.id, d.name) for d in departments]
    form.department_id.data = current_department.id
    
    classes = Class.query.filter_by(department_id=current_department.id).all()
    form.class_id.choices = [(c.id, f"Year {c.year}") for c in classes]
    form.class_id.data = current_class.id
    
    if form.validate_on_submit():
        course.code = form.code.data
        course.name = form.name.data
        course.class_id = form.class_id.data
        
        # Update session values
        session['last_university_id'] = form.university_id.data
        session['last_faculty_id'] = form.faculty_id.data
        session['last_department_id'] = form.department_id.data
        session['last_class_id'] = form.class_id.data
        
        try:
            db.session.commit()
            flash('Course updated successfully!', 'success')
            return redirect(url_for('courses.list_courses'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating course: {str(e)}', 'danger')
    
    return render_template('courses/edit_course.html', form=form, course=course, title='Edit Course')

@courses.route('/courses/<int:course_id>/delete', methods=['POST'])
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    
    try:
        db.session.delete(course)
        db.session.commit()
        flash('Course deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting course: {str(e)}', 'danger')
    
    return redirect(url_for('courses.list_courses'))