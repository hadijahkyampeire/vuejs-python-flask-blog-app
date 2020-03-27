from flask import Blueprint
from flask_restful import Api
from .views import RegisterView, LoginView, LogoutView, ResetPasswordView, EmailView

auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')
blog_api = Api(auth)

blog_api.add_resource(RegisterView, '/register')
blog_api.add_resource(LoginView, '/login')
blog_api.add_resource(LogoutView, '/logout')
blog_api.add_resource(EmailView, '/email')
blog_api.add_resource(ResetPasswordView, '/reset_password')