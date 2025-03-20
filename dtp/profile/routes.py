from flask import render_template, request, g

from . import profile

@profile.route("/", methods=["GET", "POST"])
def view():
    return render_template("profile/profile.html")

@profile.route("/edit", methods=["GET", "POST"])
def edit():
    return render_template("profile/edit_profile.html")
