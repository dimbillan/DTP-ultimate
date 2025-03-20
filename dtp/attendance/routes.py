from flask import url_for, redirect, flash, render_template, request, g, jsonify
from flask_login import current_user, login_user

from dtp import db, bcrypt, logger
from dtp.models import Student, University, Faculty, Department, Class
from dtp.auth.forms import LoginForm, RegisterForm
from dtp.auth.utils import send_reset_email

from . import attendance

@attendance.route("/list_absences", methods=["GET", "POST"])
def list_absences():
    return "List Absences"

@attendance.route("/view_stats", methods=["GET", "POST"])
def view_stats():
    return "View Stats"

@attendance.route("/add_absence", methods=["GET", "POST"])
def add_absence():
    return "add_absence"