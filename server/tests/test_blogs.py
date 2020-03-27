import unittest
import json
from api import app, db
from api.config import app_config
from api.blogs.models import blogs

class blogsTestCase(unittest.TestCase):
    """This represents the blogs testcase"""

    def setUp(self):
        # binds the app to the current context
        self.client = app.test_client()
        self.blog = {'title': 'my journey', 'blog':'To Andela'}
        with app.app_context():
            # create all database tables
            db.create_all()

    def register_user(self, username="haddie", email="user@test.com", password="test1234"):
        """This helper method helps register a test user."""
        user_data = {
            'username':username,
            'email': email,
            'password': password
        }
        return self.client.post('/api/v1/auth/register', data=user_data)

    def login_user(self, email="user@test.com", password="test1234"):
        """This helper method helps log in a test user."""
        user_data = {
            'email': email,
            'password': password
        }
        return self.client.post('/api/v1/auth/login', data=user_data)

    def test_blogs_creation(self):
        """Test the API can create blogs"""
        self.register_user()
        result = self.login_user()
        # obtain the access token
        access_token = json.loads(result.data.decode())['access_token']
        result = self.client.post('/api/v1/blog/blogs',
            headers=dict(Authorization="Bearer " + access_token), data=self.blog)
        self.assertEqual(result.status_code, 201)
        self.assertIn('blog successfully created', str(result.data))

    def test_blogs_fetching(self):
        """Test the API can get blogs"""
        self.register_user()
        result = self.login_user()
        # obtain the access token
        access_token = json.loads(result.data.decode())['access_token']
        result = self.client.post('/api/v1/blog/blogs', headers=dict(Authorization="Bearer " + access_token),data=self.blog)
        result = self.client.get('/api/v1/blog/blogs', headers=dict(Authorization="Bearer " + access_token),)
        self.assertEqual(result.status_code, 200)

    def test_blogs_can_be_got_by_id(self):
        """Test the API can get one blog"""
        self.register_user()
        result = self.login_user()
        # obtain the access token
        access_token = json.loads(result.data.decode())['access_token']
        result = self.client.post('/api/v1/blog/blogs', headers=dict(Authorization="Bearer " + access_token),data=self.blog)
        result = self.client.get('/api/v1/blog/blogs/1', headers=dict(Authorization="Bearer " + access_token),)
        self.assertEqual(result.status_code, 200)

    def test_blog_can_be_edited(self):
        """Test the API can allow edit"""
        self.register_user()
        result = self.login_user()
        # obtain the access token
        access_token = json.loads(result.data.decode())['access_token']
        result1 = self.client.post('/api/v1/blog/blogs',headers=dict(Authorization="Bearer " + access_token), data=self.blog)
        new_data = {'title':'dreams', 'blog':'to be a millionaire'}
        result2 = self.client.put('/api/v1/blog/blogs/1',headers=dict(Authorization="Bearer " + access_token), data=new_data)
        self.assertEqual(result2.status_code, 201)

    def test_blog_can_be_deleted(self):
        """Test the API can allow delete of a blog"""
        self.register_user()
        result = self.login_user()
        # obtain the access token
        access_token = json.loads(result.data.decode())['access_token']
        result = self.client.post('/api/v1/blog/blogs',
            headers=dict(Authorization="Bearer " + access_token), data=self.blog)
        result = self.client.delete('/api/v1/blog/blogs/1', headers=dict(Authorization="Bearer " + access_token),)
        self.assertEqual(result.status_code, 200)

    def test_blog_to_be_deleted_is_not_found(self):
        """Test the API can not allow delete of a blog"""
        self.register_user()
        result = self.login_user()
        # obtain the access token
        access_token = json.loads(result.data.decode())['access_token']
        result = self.client.delete('/api/v1/blog/blogs/1', 
            headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(result.status_code, 404)

    def test_blog_to_be_edited_is_not_found(self):
        """Test the API can not allow edit of a blog"""
        self.register_user()
        result = self.login_user()
        # obtain the access token
        access_token = json.loads(result.data.decode())['access_token']
        new_data = {'title':'dreams', 'blog':'to be a millionaire'}
        result = self.client.put('/api/v1/blog/blogs/1',
            headers=dict(Authorization="Bearer " + access_token), data=new_data)
        self.assertEqual(result.status_code, 404)

    def test_blog_to_be_got_is_not_found(self):
        """Test the API can not allow getting of a blog"""
        self.register_user()
        result = self.login_user()
        # obtain the access token
        access_token = json.loads(result.data.decode())['access_token']
        result = self.client.get('/api/v1/blog/blogs/1', 
            headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(result.status_code, 404)
    
    def test_user_cannot_add_blogs_with_no_token(self):
        """Test APi handles error when posting with no token"""
        result = self.client.post('/api/v1/blog/blogs', data=self.blog)
        self.assertEqual(result.status_code, 401)

    def test_user_cannot_get_blogs_with_no_token(self):
        """Test APi handles error when getting blogs with no token"""
        add = self.client.post('/api/v1/blog/blogs', data=self.blog)
        result = self.client.get('/api/v1/blog/blogs')
        self.assertEqual(result.status_code, 401)

    def test_user_cannot_edit_blogs_with_no_token(self):
        """Test APi handles error when puting with no token"""
        res = self.client.post('/api/v1/blog/blogs', data=self.blog)
        new_data={'title':'one step','blog':'beyonce'}
        result = self.client.put('/api/v1/blog/blogs/1', data=new_data)
        self.assertEqual(result.status_code, 401)

    def test_user_cannot_get_blog_by_id_with_no_token(self):
        """Test APi handles error when getting a blog with no token"""
        result1 = self.client.post('/api/v1/blog/blogs', data=self.blog)
        result = self.client.get('/api/v1/blog/blogs/1', data=self.blog)
        self.assertEqual(result.status_code, 401)

    def test_user_cannot_delete_blogs_with_no_token(self):
        """Test APi handles error when delete with no token"""
        result1 = self.client.post('/api/v1/blog/blogs', data=self.blog)
        result = self.client.delete('/api/v1/blog/blogs/1')
        self.assertEqual(result.status_code, 401)

    def test_user_has_an_invalid_token_when_posting(self):
        """Test for posting blog with invalid token"""
        access_token="bchjkngs"
        result = self.client.post('/api/v1/blog/blogs', 
                headers=dict(Authorization="Bearer " + access_token),
                    data=self.blog)
        self.assertEqual(result.status_code, 401)
    
    def test_user_has_an_invalid_token_when_getting(self):
        """Test for getting blog with invalid token"""
        access_token="bchjkngs"
        result = self.client.get('/api/v1/blog/blogs', 
                headers=dict(Authorization="Bearer " + access_token),
                    data=self.blog)
        self.assertEqual(result.status_code, 401)

    def test_user_has_an_invalid_token_when_getting_one(self):
        """Test for getting one blog with invalid token"""
        access_token="bchjkngs"
        result = self.client.post('/api/v1/blog/blogs', 
                headers=dict(Authorization="Bearer " + access_token),
                    data=self.blog)
        result = self.client.get('/api/v1/blog/blogs/1', 
                headers=dict(Authorization="Bearer " + access_token),
                    data=self.blog)
        self.assertEqual(result.status_code, 401)

    def test_user_has_an_invalid_token_when_getting_one(self):
        """Test for getting one blog with invalid token"""
        access_token="bchjkngs"
        result = self.client.post('/api/v1/blog/blogs', 
                headers=dict(Authorization="Bearer " + access_token),
                    data=self.blog)
        result = self.client.get('/api/v1/blog/blogs/1', 
                headers=dict(Authorization="Bearer " + access_token),
                    data=self.blog)
        self.assertEqual(result.status_code, 401)

    def test_user_has_an_invalid_token_when_deleting_one(self):
        """Test for deleting one blog with invalid token"""
        access_token="bchjkngs"
        result = self.client.post('/api/v1/blog/blogs', 
                headers=dict(Authorization="Bearer " + access_token),
                    data=self.blog)
        result = self.client.delete('/api/v1/blog/blogs/1', 
                headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(result.status_code, 401)

    def test_user_has_an_invalid_token_when_putting_one(self):
        """Test for putting one blog with invalid token"""
        access_token="bchjkngs"
        result = self.client.post('/api/v1/blog/blogs', 
                headers=dict(Authorization="Bearer " + access_token),
                    data=self.blog)
        new_blog={"title":"memories", "blog":"my own"}
        result = self.client.put('/api/v1/blog/blogs/1', 
                headers=dict(Authorization="Bearer " + access_token),
                    data=new_blog)
        self.assertEqual(result.status_code, 401)

    def tearDown(self):
        with app.app_context():
            # create all database tables
            db.session.remove()
            db.drop_all()