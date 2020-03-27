import jwt
import datetime
from datetime import timedelta, datetime
from api import db
from flask import current_app
from flask_bcrypt import Bcrypt

class User(db.Model):
    # Define the columns of the users table, starting with the primary key
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    blogs = db.relationship(
        'blogs', order_by='blogs.id', cascade="all, delete-orphan", lazy='dynamic')
        
    def __init__(self, email, password, username):
        """Initialize the user with an email and a password."""
        self.email = email
        self.username = username
        self.password = Bcrypt().generate_password_hash(password).decode()

    def password_is_valid(self, password):
        """
        Checks the password against it's hash to validates the user's password
        """
        return Bcrypt().check_password_hash(self.password, password)

    def save(self):
        """Save a user to the database.
        This includes creating a new user and editing one.
        """
        db.session.add(self)
        db.session.commit()

    def generate_token(self, user_id):
        """ Generates the access token"""
        try:
            # set up a payload with an expiration time
            payload = {
                'exp': datetime.utcnow() + timedelta(days=30),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            # create the byte string token using the payload and the SECRET key
            jwt_string = jwt.encode(
                payload,
                current_app.config.get('SECRET_KEY'),
                algorithm='HS256'
            ).decode('utf-8')
            return jwt_string
        except Exception as e:
            # return an error in string format if an exception occurs
            return str(e)

    @staticmethod
    def decode_token(token):
        """Decodes the access token from the Authorization header."""
        try:
            # try to decode the token using our SECRET variable
            payload = jwt.decode(token, current_app.config.get('SECRET_KEY'))
            token_is_revoked = RevokedToken.check_revoked_token(auth_token=token)
            if token_is_revoked:
                return 'Revoked token. please login to get a new token'
            return payload['sub']
        except jwt.ExpiredSignatureError:
            # the token is expired, return an error string
            return "Expired token. Please login to get a new token"
        except jwt.InvalidTokenError:
            # the token is invalid, return an error string
            return "Invalid token. Please register or login"
    def __repr__(self):
        return "<User: {}>".format(self.email)


class RevokedToken(db.Model):
    """Define the 'RevokedToken' model mapped to database table 'revoked_tokens'."""

    __tablename__ = 'revoked_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    revoked_on = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)

    def __init__(self, token):
        self.token = token

    def save(self):
        """Save to database table"""
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def check_revoked_token(auth_token):
        """function to check if token is revoked
        """
        # check whether token has been revoked
        res = RevokedToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

class blogs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    blog = db.Column(db.String(100))
    created_by = db.Column(db.Integer, db.ForeignKey(User.id))
    created_on = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        """defines the representation of an object"""
        return "blogs: {}".format(self.title)

    def save(self):
        """defines the save method for the blogs"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """defines the delete method for the blogs"""
        db.session.delete(self)
        db.session.commit()