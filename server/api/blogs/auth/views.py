import os
import datetime
import jwt

from flask import jsonify, make_response, Flask, request
from flask_restful import Resource
from flask_mail import Mail, Message
from flask_bcrypt import Bcrypt

from webargs.flaskparser import use_args
from api.blogs.args import user_args, login_args, email_args, reset_password
from api.blogs.models import User, RevokedToken

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ.get('SECRET_KEY')
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

recipients = []
class RegisterView(Resource):
    """Register view"""
    @use_args(user_args, locations={'json', 'form'})
    def post(self, args):
        try:
            new_user =User(
                username=args['username'],
                email=args['email'],
                password=args['password']
            )
            print(new_user)
            print(args['username'])
            user= User.query.filter_by(email=args['email']).first()
            if user:
                return make_response(jsonify({
                    'message':'User already exists please login'
                }), 409)
            new_user.save()
            response = {'message':'You successfully registered'}
            return make_response(jsonify(response), 201)
        except Exception as e:  # pragma: no cover
            # An error occured, then return a message containing the error
            return make_response(jsonify({'message': 'Invalid data,'
                            ' something is wrong'}), 400)
    
class LoginView(Resource):
    """Login view"""
    @use_args(login_args, locations={'json', 'form'})
    def post(self, args):
        try:
            user= User.query.filter_by(email=args['email']).first()
            if user and user.password_is_valid(args['password']):
                # Generate the access token to be used as the header
                access_token = user.generate_token(user.id)
                if access_token:
                    return make_response(jsonify({'message': 
                        'You logged in successfully.',
                        'access_token': access_token,
                        'user_email': user.email,
                        'username': user.username,
                        'Id': user.id}
                        ), 200)

            return make_response(jsonify({'message': 'Invalid email or password,'
                            ' Please try again'}), 401)
        except Exception as e:  # pragma: no cover
            # Create a response containing an string error message
            return make_response(jsonify({'message': 
                'An error occured'
                ' ensure proper login'}), 401)

class LogoutView(Resource):
    def post(self):
        """This route handles logout """
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return make_response(jsonify({"message": "No token,"
                            " please provide a token"}), 401)
        access_token = auth_header.split()[1]
        if access_token:
            user_id = User.decode_token(access_token)
            if isinstance(user_id, int):
                revoked_token = RevokedToken(token=access_token)
                revoked_token.save()
                return make_response(jsonify({'message': 'Your have been logged out.'}), 201)
            else:
                message = user_id
                response = {'message': message}
                return make_response(jsonify(response), 401)
        else:
            return make_response(jsonify({'message': 'please provide a  valid token'}), 401)

class EmailView(Resource):
    """ This will send an email with the token to reset password."""
    @use_args(email_args, locations={'json', 'form'})
    def post(self, args):
    # This method will edit the already existing password
        user = User.query.filter_by(email=args['email']).first()
        if not user:
            return make_response(jsonify({'message': 'User does not exist!'}), 404)
        print(user)
        try:
            access_token = jwt.encode({'id': user.id, 'expiry_time': str(datetime.datetime.utcnow() +
            datetime.timedelta(minutes=30))},
            os.environ.getenv('SECRET_KEY'))
            print(access_token)
            subject = "Yummy Recipes Reset Password"
            recipients.append(email)
            msg = Message(subject, sender="Admin", recipients=recipients)
            styles = "background-color:blue; color:white; padding: 5px 10px; border-radius:3px; text-decoration: none;"
            msg.html = f"Click the link to reset password:\n \n<h3><a href='https://hadijahz-recipes-react.herokuapp.com/reset?tk={access_token.decode()}' style='{styles}'>Reset Password</a></h3>"
            with app.app_context():
                mail.send(msg)
            return make_response(jsonify({'message': 'Password Reset link sent successfully to '+email+''}), 201)
        except Exception:
            return make_response(jsonify({'message': 'Invalid request sent.'}), 400)

class ResetPasswordView(Resource):
    """This class will handle the resetting of password"""
    @use_args(reset_password, locations={'json', 'form'})
    def put(self):
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return jsonify({"message": "No token,"
                            " please provide a token"}), 401
        access_token = auth_header.split()[1]
        if access_token:
            # This method will edit the already existing password
            new_user =User(
                email=args['email'].strip(),
                password=args['password'].strip(),
                retyped_password=args['retyped_password'].strip()
            )
            if password != retyped_password:
                return make_response(jsonify({'message': 'Password mismatch'}), 400)
            user = User.query.filter_by(email=args['email']).first()
            if user:
                user.password = Bcrypt().generate_password_hash(retyped_password).decode()
                user.save()
                return make_response(jsonify({'message': 'Password resetting is successful'}), 200)
            return make_response(jsonify({'message': 'User does not exist!'}), 404)
        return make_response(jsonify({'message': 'please provide a  valid token'}), 401)