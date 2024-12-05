from marshmallow import fields, validate
from app.schemas.base import BaseSchema

class NotificationSchema(BaseSchema):
    user_id = fields.Int(required=True)
    message = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    timestamp = fields.DateTime(dump_only=True)

    user = fields.Nested('UserSchema', dump_only=True)

    @post_load
    def make_notification(self, data, **kwargs):
        return Notification(**data)