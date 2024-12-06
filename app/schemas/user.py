from marshmallow import fields, validate
from app.schemas.base import BaseSchema
from ..models import User , UserProfile

class UserSchema(BaseSchema):
    username = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    email = fields.Str(required=True, validate=validate.Email())
    password_hash = fields.Str(load_only=True, required=True)
    role = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    profile = fields.Nested('UserProfileSchema', dump_only=True)

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)

class UserProfileSchema(BaseSchema):
    first_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    last_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    user_id = fields.Int(required=True)

    @post_load
    def make_profile(self, data, **kwargs):
        return UserProfile(**data)