from flask import render_template, request, g

from . import core


@core.before_request
def get_real_ip():
    g.real_ip = (
        request.headers.get("X-Real-IP")
        or request.headers.get("X-Forwarded-For")
        or request.remote_addr
    )

@core.route("/")
@core.route("/home")
@core.route("/index")
def index():    
        return render_template("core/index.html", title="Anasayfa")

@core.route("/dashboard")
def dashboard():    
        return render_template("core/dashboard.html", title="Dashboard")