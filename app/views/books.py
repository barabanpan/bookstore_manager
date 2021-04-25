from flask.blueprints import Blueprint
from flask import render_template, session


books_bp = Blueprint('books', __name__)


@books_bp.route("/books")
def books():
    return render_template("books.html", welcome_user=session.get("email"))
