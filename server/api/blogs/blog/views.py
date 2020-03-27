from flask import jsonify, make_response, request
from flask_restful import Resource
from webargs.flaskparser import use_args
from api.blogs.args import blogs_args
from api.blogs.models import blogs, User

class blogsListView(Resource):
    """blogs view"""
    @use_args(blogs_args, locations={'json', 'form'})
    def post(self, args):
        auth_header = request.headers.get('Authorization', None)
        if auth_header is None:
            return make_response(jsonify({"message": "No token, please provide a token"}), 401)
        access_token = auth_header.split(" ")[1]
        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str): 
                new_blog=blogs(
                    title=args['title'],
                    blog=args['blog']
                )
                new_blog.created_by = user_id
                new_blog.save()
                response = {'message':'blog successfully created'}
                return make_response(jsonify(response), 201)
            return make_response(jsonify({'message': user_id}),401)

    def get(self):
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return make_response(jsonify({"message": "No token, please provide a token"}), 401)
        access_token = auth_header.split(" ")[1]
        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                blogposts = blogs.query.filter_by(created_by=user_id)
                items=[]
                for blog in blogposts:
                    blog_data={}
                    blog_data['id']=blog.id
                    blog_data['title']=blog.title
                    blog_data['blog']=blog.blog
                    blog_data['created_by']=blog.created_by
                    items.append(blog_data)

                response={'blog_items':items}
                return make_response(jsonify(response), 200)
            return make_response(jsonify({'message': user_id}),401)

class blogDetailsView(Resource):
    """blog details"""
    def get(self, blog_id):
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return make_response(jsonify({"message": "No token, please provide a token"}), 401)
        access_token = auth_header.split(" ")[1]
        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                blog= blogs.query.filter_by(id=blog_id, created_by=user_id).first()
                if not blog:
                    return make_response(jsonify({
                        'message':'no blog found by id'
                    }), 404)
                response = {
                    'blog':{
                        'id':blog.id,
                        'title':blog.title,
                        'blog':blog.blog
                    }
                }
                return make_response(jsonify(response), 200)
            return make_response(jsonify({'message': user_id}),401)

    def delete(self, blog_id):
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return make_response(jsonify({"message": "No token, please provide a token"}), 401)
        access_token = auth_header.split(" ")[1]
        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                blog = blogs.query.filter_by(id=blog_id, created_by=user_id).first()
                if not blog:
                    return make_response(jsonify({
                        'message':'no blog found by id'
                    }), 404)
                blog.delete()
                return make_response(jsonify({
                    'message':'blog successfully deleted'
                }), 200)
            return make_response(jsonify({'message': user_id}), 401)

    @use_args(blogs_args, locations={'json', 'form'})
    def put(self, args, blog_id):
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return make_response(jsonify({"message": "No token, please provide a token"}), 401)
        access_token = auth_header.split(" ")[1]
        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                blog = blogs.query.filter_by(id=blog_id, created_by=user_id).first()
                if not blog:
                    return make_response(jsonify({
                        'message':'no blog found by id'
                    }), 404)
                blog.title=args['title']
                blog.blog= args['blog']
                blog.save()
                response = {
                    'blog':{
                        'id':blog.id,
                        'title':blog.title,
                        'blog':blog.blog
                    }
                }
                return make_response(jsonify(response), 201)
            return make_response(jsonify({'message': user_id}),401)

