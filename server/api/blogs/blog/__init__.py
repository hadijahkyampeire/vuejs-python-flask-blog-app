from flask import Blueprint
from flask_restful import Api
from .views import blogsListView, blogDetailsView

blog = Blueprint('blog', __name__, url_prefix='/api/v1/blog')
blog_api = Api(blog)

blog_api.add_resource(blogsListView, '/blogs')
blog_api.add_resource(blogDetailsView, '/blogs/<int:blog_id>')