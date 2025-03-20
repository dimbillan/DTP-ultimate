from . import profile

@profile.route("/profile", methods=["GET", "POST"])
def view_profile():
    return "View Profile"