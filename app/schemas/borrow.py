from marshmallow import fields, validate
from app.schemas.base import BaseSchema
from ..models import BorrowRecord , BorrowHistory

class BorrowRecordSchema(BaseSchema):
    user_id = fields.Int(required=True)
    book_id = fields.Int(required=True)
    status = fields.Str(required=True)
    borrow_date = fields.DateTime(required=True)
    return_date = fields.DateTime()

    user = fields.Nested('UserSchema', dump_only=True)
    book = fields.Nested('BookSchema', dump_only=True)

    @post_load
    def make_borrow_record(self, data, **kwargs):
        return BorrowRecord(**data)

class BorrowHistorySchema(BaseSchema):
    borrow_record_id = fields.Int(required=True)
    status = fields.Str(required=True, validate=validate.OneOf(["returned", "overdue"]))
    updated_at = fields.DateTime(dump_only=True)

    borrow_record = fields.Nested(BorrowRecordSchema, dump_only=True)

    @post_load
    def make_borrow_history(self, data, **kwargs):
        return BorrowHistory(**data)
