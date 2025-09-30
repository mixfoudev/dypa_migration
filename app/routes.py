from flask import Blueprint, render_template, request
from .db import queries

main = Blueprint("main", __name__)

@main.route("/", methods=["GET", "POST"])
def index():
    users = queries.get_users()
    return render_template("index.html", users=users)
