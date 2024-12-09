from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from utils import (
    create_new_user,
    get_all_borrow_requests,
    approve_or_deny_borrow_request,
    get_user_borrow_history_for_librarian,
    format_response,
    make_error_response
)
from schemas import UserSchema, BorrowRecordSchema, BorrowHistorySchema

# Define Blueprint for librarian routes
librarian_bp = Blueprint('librarian_bp', __name__)

# ========================
# Routes for Librarians
# ========================

@librarian_bp.route('/librarian/user', methods=['POST'])
@jwt_required()
def create_user():
    """
    Create a new library user with an email, password, and role.
    """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'user')  # Default role is 'user'

    # Validate input
    if not email or not password:
        return make_error_response("Email and password are required.", 400)

    # Create the user
    response, status_code = create_new_user(email, password, role)
    if status_code == 201:
        user_schema = UserSchema()
        return jsonify(format_response(response, user_schema)), 201
    else:
        return make_error_response(response.get("error"), status_code)


@librarian_bp.route('/librarian/requests', methods=['GET'])
@jwt_required()
def view_all_borrow_requests():
    """
    View all book borrow requests.
    """
    # Get borrow requests from the utility function
    borrow_requests = get_all_borrow_requests()
    if isinstance(borrow_requests, tuple):  # Error response
        return make_error_response(borrow_requests[0], borrow_requests[1])

    borrow_request_schema = BorrowRecordSchema(many=True)
    return jsonify(format_response(borrow_requests, borrow_request_schema)), 200


@librarian_bp.route('/librarian/requests/<int:request_id>', methods=['PATCH'])
@jwt_required()
def manage_borrow_request(request_id):
    """
    Approve or deny a borrow request.
    """
    data = request.get_json()
    status = data.get('status')

    # Validate input
    if not status or status not in ['Approved', 'Denied']:
        return make_error_response("Invalid status. Use 'Approved' or 'Denied'.", 400)

    # Approve or deny the request
    response, status_code = approve_or_deny_borrow_request(request_id, status)
    if status_code == 200:
        borrow_request_schema = BorrowRecordSchema()
        return jsonify(format_response(response, borrow_request_schema)), 200
    else:
        return make_error_response(response.get("error"), status_code)


@librarian_bp.route('/librarian/users/<int:user_id>/history', methods=['GET'])
@jwt_required()
def view_user_borrow_history(user_id):
    """
    View a specific user's book borrow history.
    """
    history = get_user_borrow_history_for_librarian(user_id)
    if isinstance(history, tuple):  # Error response
        return make_error_response(history[0], history[1])

    borrow_history_schema = BorrowHistorySchema(many=True)
    return jsonify(format_response(history, borrow_history_schema)), 200
