from flask.blueprints import Blueprint
from flask import render_template, session, request, redirect

from app.models.book_model import BookModel


books_bp = Blueprint('books', __name__, url_prefix="/books")


@books_bp.route("/")
def books():
    books = BookModel.return_all()
    return render_template("books/books.html", books=books, 
                           welcome_user=session.get("email"))


@books_bp.route("/add", methods=['GET', 'POST'])
def add_book():
    if request.method == "GET":
        return render_template("books/add_book.html", welcome_user=session.get("email"))

    title = request.form.get("title")
    author = request.form.get("author")
    year = request.form.get("year")
    description = request.form.get("description")

    new_book = BookModel(title, author, year, description)
    new_book.save_to_db()

    return redirect("/books/")


@books_bp.route("/update", methods=['GET', 'POST'])
def update_book():
    if request.method == "GET":
       id_ = request.args.get("id")
       book = BookModel.find_by_id(id_)
       return render_template("books/update_book.html", book=book, welcome_user=session.get("email"))

    id_ = request.form.get("id")
    title = request.form.get("title")
    author = request.form.get("author")
    year = request.form.get("year")
    description = request.form.get("description")

    book = BookModel.find_by_id(id_)
    book.update(title, author, year, description)

    return redirect("/books/")


@books_bp.route("/delete")
def delete_book():
    answer = request.args.get("answer")
    id_ = request.args.get("id")
    if not answer:
        book = BookModel.find_by_id(id_)
        return render_template("books/delete_book.html", book=book, welcome_user=session.get("email"))

    if answer == "yes":
        BookModel.delete_by_id(id_)
        return redirect("/books/")
    elif answer == "cancel":
        return redirect("/books/")
