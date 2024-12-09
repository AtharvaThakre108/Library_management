from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow import fields
from models import User, UserProfile, Book, Author, BorrowRecord, BorrowHistory 

class UserProfileSchema(SQLAlchemySchema):
    class Meta:
        model = UserProfile
        load_instance = True  # Deserialize to model instances

    id = auto_field()
    user_id = auto_field()
    first_name = auto_field()
    last_name = auto_field()


class UserSchema(SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True

    id = auto_field()
    username = auto_field()
    email = auto_field()
    password_hash = fields.String(load_only=True)  # Exclude from output for security
    role = auto_field()
    profile = fields.Nested(UserProfileSchema, many=False)


class AuthorSchema(SQLAlchemySchema):
    class Meta:
        model = Author
        load_instance = True

    id = auto_field()
    name = auto_field()
    books = fields.List(fields.Nested("BookSchema", exclude=("author",)))  # Prevent circular reference


class BookSchema(SQLAlchemySchema):
    class Meta:
        model = Book
        load_instance = True

    id = auto_field()
    title = auto_field()
    author_id = auto_field()
    author = fields.Nested(AuthorSchema, only=("id", "name"))
    isbn = auto_field()
    published_date = auto_field()


class BorrowRecordSchema(SQLAlchemySchema):
    class Meta:
        model = BorrowRecord
        load_instance = True

    id = auto_field()
    user_id = auto_field()
    book_id = auto_field()
    status = auto_field()
    borrow_date = auto_field()
    return_date = auto_field()
    user = fields.Nested(UserSchema, only=("id", "username"))
    book = fields.Nested(BookSchema, only=("id", "title"))


class BorrowHistorySchema(SQLAlchemySchema):
    class Meta:
        model = BorrowHistory
        load_instance = True

    id = auto_field()
    borrow_record_id = auto_field()
    status = auto_field()
    updated_at = auto_field()
    borrow_record = fields.Nested(BorrowRecordSchema, only=("id", "status"))
