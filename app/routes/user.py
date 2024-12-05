from flask import request
from flask_restful import Resource
from app.models import db, User, UserProfile
from app.schemas import UserSchema, UserProfileSchema

user_schema = UserSchema()
users_schema = UserSchema(many=True)
profile_schema = UserProfileSchema()

class UserResource(Resource):
    def get(self, user_id=None):
        if user_id:
            user = User.query.get_or_404(user_id)
            return user_schema.dump(user), 200
        users = User.query.all()
        return users_schema.dump(users), 200

    def post(self):
        data = request.json
        user = user_schema.load(data)
        db.session.add(user)
        db.session.commit()
        return user_schema.dump(user), 201

    def put(self, user_id):
        user = User.query.get_or_404(user_id)
        data = request.json
        for key, value in data.items():
            setattr(user, key, value)
        db.session.commit()
        return user_schema.dump(user), 200

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted"}, 204

class UserProfileResource(Resource):
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        profile = user.profile
        return profile_schema.dump(profile), 200

    def put(self, user_id):
        user = User.query.get_or_404(user_id)
        data = request.json
        profile = user.profile
        if profile:
            for key, value in data.items():
                setattr(profile, key, value)
        else:
            profile = profile_schema.load(data)
            profile.user_id = user_id
            db.session.add(profile)
        db.session.commit()
        return profile_schema.dump(profile), 200
