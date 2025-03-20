from flask import url_for, redirect, flash, render_template, request, g
from flask_login import current_user, login_user, logout_user

from dtp import db
from dtp.models import Student, University, Faculty, Department, Class
from dtp.auth.forms import LoginForm, RegisterForm
from dtp.auth.utils import send_reset_email, log

from . import auth


@auth.before_request
def get_real_ip():
    g.real_ip = (
        request.headers.get("X-Real-IP")
        or request.headers.get("X-Forwarded-For")
        or request.remote_addr
    )


@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("core.index"))

    form = LoginForm()

    if form.validate_on_submit():
        student = Student.query.filter_by(email=form.email.data).first()

        if student and student.verify_password(form.password.data):
            login_user(student)
            log(request.method, g.real_ip, request.path, current_user.first_name, current_user.id, "User logged in")
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("core.index"))
        else:
            log(request.method, g.real_ip, request.path, form.email.data, None, "Login failed")
            flash(
                "Giriş Başarısız. Öğrenci numaranızı ve şifrenizi kontrol edin.",
                "danger",
            )

    return render_template("auth/login.html", title="Giriş Yap", form=form)


@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    
    # Populate university and class choices
    form.university.choices = [(u.id, u.name) for u in University.query.all()]
    
    # Populate faculty choices if university is selected
    if form.university.data:
        form.faculty.choices = [(f.id, f.name) for f in Faculty.query.filter_by(university_id=form.university.data).all()]
    else:
        form.faculty.choices = [('', 'Önce Üniversite Seçin')]
    
    # Populate department choices if faculty is selected
    if form.faculty.data:
        form.department.choices = [(d.id, d.name) for d in Department.query.filter_by(faculty_id=form.faculty.data).all()]
    else:
        form.department.choices = [('', 'Önce Fakülte Seçin')]

    # Populate class choices if department is selected
    if form.department.data:
        form.class_year.choices = [(c.id, c.year) for c in Class.query.filter_by(department_id=form.department.data).all()]
    else:
        form.class_year.choices = [('', 'Önce Bölüm Seçin')]

    if form.validate_on_submit():
        student = Student(
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            student_number=form.student_number.data,
            university_id=form.university.data,
            faculty_id=form.faculty.data,
            department_id=form.department.data,
            class_id=form.class_year.data,
            password=form.password.data,
        )
        db.session.add(student)
        db.session.commit()

        log(request.method, g.real_ip, request.path, student.first_name , student.id, "User registered")

        flash("Hesabınız başarıyla oluşturuldu. Giriş yapabilirsiniz.", "success")
        return redirect(url_for("auth.login"))
    
    return render_template("auth/register.html", title="Kayıt Ol", form=form)

@auth.route("/logout")
def logout():
    log(request.method, g.real_ip, request.path, current_user.first_name, current_user.id, "User logged out")
    logout_user()
    return redirect(url_for("core.index"))

@auth.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    return redirect(url_for("core.index"))