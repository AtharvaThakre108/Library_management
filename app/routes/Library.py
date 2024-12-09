from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils import (
    get_all_books,
    request_to_borrow_book,
    get_user_borrow_history,
    format_response,
    make_error_response
)
from schemas import BookSchema, BorrowRecordSchema

# Define Blueprint for library routes
library_bp = Blueprint('library_bp', __name__)

# ========================
# Routes for Library Users
# ========================

@library_bp.route('/library/books', methods=['GET'])
@jwt_required()
def list_books():
    """
    Get a list of all books in the library.
    """
    try:
        books = get_all_books()
        if isinstance(books, tuple):  # Handle errors from the utility function
            return make_error_response(books[0], books[1])

        book_schema = BookSchema(many=True)
        return jsonify(format_response(books, book_schema)), 200
    except Exception as e:
        return make_error_response(f"An error occurred: {str(e)}", 500)


@library_bp.route('/library/borrow', methods=['POST'])
@jwt_required()
def borrow_book():
    """
    Submit a request to borrow a book for specific dates.
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    book_id = data.get('book_id')
    borrow_date_start = data.get('borrow_date_start')
    borrow_date_end = data.get('borrow_date_end')

    # Validate input
    if not book_id or not borrow_date_start or not borrow_date_end:
        return make_error_response("Book ID and borrow dates are required.", 400)

    try:
        # Process borrow request
        response, status_code = request_to_borrow_book(user_id, book_id, borrow_date_start, borrow_date_end)
        if status_code == 201:
            borrow_record_schema = BorrowRecordSchema()
            return jsonify(format_response(response, borrow_record_schema)), 201
        else:
            return make_error_response(response.get("error"), status_code)
    except Exception as e:
        return make_error_response(f"An error occurred: {str(e)}", 500)


@library_bp.route('/library/history', methods=['GET'])
@jwt_required()
def view_borrow_history():
    """
    View the personal borrow history of the logged-in user.
    """
    user_id = get_jwt_identity()
    try:
        history = get_user_borrow_history(user_id)
        if isinstance(history, tuple):  # Handle errors from the utility function
            return make_error_response(history[0], history[1])

        borrow_record_schema = BorrowRecordSchema(many=True)
        return jsonify(format_response(history, borrow_record_schema)), 200
    except Exception as e:
        return make_error_response(f"An error occurred: {str(e)}", 500)
