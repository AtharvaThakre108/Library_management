from flask import jsonify, make_response
from datetime import datetime
from models import Book, BorrowRecord, User, BorrowHistory
from schemas import BookSchema, BorrowRecordSchema, UserSchema, BorrowHistorySchema
from app import db

# ========================
# Library User Utilities
# ========================

def get_all_books():
    """
    Retrieve a list of all books in the library.
    """
    books = Book.query.all()
    schema = BookSchema(many=True)
    return schema.dump(books), 200


def request_to_borrow_book(user_id, book_id, start_date, end_date):
    """
    Handle a borrow request from a library user.
    """
    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        return make_error_response("Invalid date format. Use YYYY-MM-DD.", 400)

    # Check if the book is already borrowed for the requested dates
    overlapping_request = BorrowRecord.query.filter(
        BorrowRecord.book_id == book_id,
        BorrowRecord.status == 'Approved',
        BorrowRecord.borrow_date <= end_date,
        BorrowRecord.return_date >= start_date
    ).first()

    if overlapping_request:
        return make_error_response("The book is already borrowed for the requested dates.", 400)

    # Create a new borrow request
    borrow_record = BorrowRecord(
        user_id=user_id,
        book_id=book_id,
        status="pending",
        borrow_date=start_date,
        return_date=end_date
    )
    db.session.add(borrow_record)
    db.session.commit()

    schema = BorrowRecordSchema()
    return schema.dump(borrow_record), 201


def get_user_borrow_history(user_id):
    """
    Retrieve the borrow history of a specific user.
    """
    history = BorrowHistory.query.join(BorrowRecord).filter(BorrowRecord.user_id == user_id).all()
    schema = BorrowHistorySchema(many=True)
    return schema.dump(history), 200


# ========================
# Librarian Utilities
# ========================

def create_new_user(email, password, role="user"):
    """
    Create a new library user with the provided email and password.
    """
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return make_error_response("User with this email already exists.", 400)

    new_user = User(email=email, password_hash=password, role=role)
    db.session.add(new_user)
    db.session.commit()

    schema = UserSchema()
    return schema.dump(new_user), 201


def get_all_borrow_requests():
    """
    Retrieve all borrow requests in the system.
    """
    requests = BorrowRecord.query.all()
    schema = BorrowRecordSchema(many=True)
    return schema.dump(requests), 200


def approve_or_deny_borrow_request(request_id, status):
    """
    Approve or deny a borrow request based on its ID.
    """
    borrow_request = BorrowRecord.query.get(request_id)
    if not borrow_request:
        return make_error_response("Borrow request not found.", 404)

    if status not in ['Approved', 'Denied']:
        return make_error_response("Invalid status. Use 'Approved' or 'Denied'.", 400)

    borrow_request.status = status
    db.session.commit()

    schema = BorrowRecordSchema()
    return schema.dump(borrow_request), 200


def get_user_borrow_history_for_librarian(user_id):
    """
    View a specific user's borrow history (for librarian use).
    """
    user = User.query.get(user_id)
    if not user:
        return make_error_response("User not found.", 404)

    history = BorrowHistory.query.join(BorrowRecord).filter(BorrowRecord.user_id == user_id).all()
    schema = BorrowHistorySchema(many=True)
    return schema.dump(history), 200


# ========================
# Helper Functions
# ========================

def format_response(data, schema, many=False):
    """
    Format the response using Marshmallow schema.
    """
    return schema(many=many).dump(data)


def make_error_response(message, status_code):
    """
    Create a standardized error response.
    """
    return make_response(jsonify({"error": message}), status_code)
