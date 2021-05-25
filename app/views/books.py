from flask.blueprints import Blueprint
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from app.models.book_model import BookModel, to_json


books_bp = Blueprint('books', __name__, url_prefix="/books")


def required_error(required_list):
    return ", ".join(r for r in required_list) + " are required", 400


@books_bp.route("/get_all", methods=["POST"])
def get_books():
    required = ["page", "limit"]

    if not request.json:
        return required_error(required)
    page = request.json.get("page")
    limit = request.json.get("limit")
    title = request.json.get("title", "")
    author = request.json.get("author", "")
    if not page or not limit:
        return required_error(required)

    books = BookModel.find_by_title_and_author(title, author, page, limit)
    return books


@books_bp.route("/<id>", methods=["GET"])
def get_book(id):
    new_book = BookModel.find_by_id(id)
    if not new_book:
        return {"message": "No such book."}, 404
    return to_json(new_book), 200


@books_bp.route("/", methods=["POST"])
@jwt_required()
def add_book():
    required = ["title", "author", "year", "price", "quantity"]

    if not request.json:
        return required_error(required)
    title = request.json.get("title")
    author = request.json.get("author")
    year = request.json.get("year")
    price = request.json.get("price")
    quantity = request.json.get("quantity")
    description = request.json.get("description", "")
    if not (title and author and year and price and quantity):
        return required_error(required)

    new_book = BookModel(title, author, year, price, quantity, description)
    new_book.save_to_db()
    return {"id": str(new_book.id)}, 200


@books_bp.route("/<id>", methods=["PUT"])
@jwt_required()
def update_book(id):
    title = request.json.get("title")
    author = request.json.get("author")
    year = request.json.get("year")
    price = request.json.get("price")
    quantity = request.json.get("quantity")
    description = request.json.get("description")

    book = BookModel.find_by_id(id)
    book.update(title, author, year, price, quantity, description)

    return to_json(book)


@books_bp.route("/<id>", methods=["DELETE"])
@jwt_required()
def delete_book(id):
    book = BookModel.find_by_id(id)
    if not book:
        return {"message": "No such book"}, 404
    BookModel.delete_by_id(id)
    return {"message": "Deleted."}, 204
