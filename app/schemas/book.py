from marshmallow import fields, validate
from app.schemas.base import BaseSchema

class BookSchema(BaseSchema):
    title = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    author_id = fields.Int(required=True)
    isbn = fields.Str(validate=validate.Length(max=20))
    published_date = fields.Str(validate=validate.Length(max=20))
    author = fields.Nested('AuthorSchema', dump_only=True)

    @post_load
    def make_book(self, data, **kwargs):
        return Book(**data)

class AuthorSchema(BaseSchema):
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    books = fields.List(fields.Nested(BookSchema), dump_only=True)

    @post_load
    def make_author(self, data, **kwargs):
        return Author(**data)
