from flask import url_for, redirect, flash, render_template, request, g
from flask_login import current_user, login_user

from dtp import db, bcrypt, logger
from dtp.models import Student, Course
from dtp.auth.forms import LoginForm
from dtp.auth.utils import send_reset_email

from . import courses

@courses.route("/list")
def list():
    courses = Student.get_available_courses(current_user)
    return render_template("courses/list.html", title="Courses", courses=courses)

@courses.route("/add_course", methods=["GET"])
def add_course():
    return render_template("courses/add_course.html", title="Add Course")

@courses.route("/add_course/<int:course_id>", methods=["POST"])
#Change this. Course must be added with name and code. NOT WITH INTeger value
def add_course_func(course_id):
    course = Course.query.get_or_404(course_id)
    current_user.courses.append(course)
    db.session.commit()
    flash("Course added successfully", "success")
    return redirect(url_for("courses.list"))

@courses.route("/remove_course/<int:course_id>")
def remove_course(course_id):
    course = Course.query.get_or_404(course_id)
    current_user.courses.remove(course)
    db.session.commit()
    flash("Course removed successfully", "success")
    return redirect(url_for("courses.list"))

