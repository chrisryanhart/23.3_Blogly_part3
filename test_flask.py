from unittest import TestCase

from app import app
from models import db, User, Post

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_users_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """User and blog post tests for flask routes"""

    def setUp(self):
        User.query.delete()

        user = User(first_name='Petry',last_name='Jones',image_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRX_FJrccL0udXqC4zEjHTBxpDZl7zztfrlmA&usqp=CAU')

        db.session.add(user)
        db.session.commit()

        post = Post(title='Rolling Stone',content='classic american rock song by bob dylan',user_id=1)

        db.session.add(post)
        db.session.commit()

        self.user_id=user.id
        self.image_url=user.image_url

        self.post_id=post.id
        self.post=post


    def tearDown(self):
        db.session.rollback()
    
    def test_post_new_user(self):
        with app.test_client() as client:
            d={"first_name":'bobby', 'last_name':'sue', 'image_url':'https://upload.wikimedia.org/wikipedia/commons/a/ae/Jimi_Hendrix_1967.png'}
            resp = client.post('/users/new',data=d,follow_redirects=True)
            html=resp.get_data(as_text=True)

            self.assertEqual(resp.status_code,200)
            self.assertIn('bobby sue',html)

    def test_show_all_users(self):
        with app.test_client() as client:
            resp=client.get('/users')
            html=resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Petry Jones', html)


    # @app.route('/users/<int:user_id>')
    def test_show_user_info(self):
        with app.test_client() as client:
            resp=client.get(f'/users/{self.user_id}')
            html=resp.get_data(as_text=True)

            self.assertEqual(resp.status_code,200)
            self.assertIn("<h3>Petry Jones</h3>",html)


    def test_delete_user(self):
        with app.test_client() as client:
            # d={'user_id': f'{self.user_id}', 'post_id'},
            resp = client.post(f'/users/{self.user_id}/delete',follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code,200)
            self.assertNotIn('Petry Jones',html)



    def test_post_form(self):
        with app.test_client() as client:
            resp=client.get(f'/users/{self.user_id}/posts/new')
            html=resp.get_data(as_text=True)

            self.assertEqual(resp.status_code,200)
            self.assertIn('<h3>Add Post for Petry Jones</h3>', html)


    def test_submit_post(self):
        with app.test_client() as client:
            resp=client.post(f'/users/{self.user_id}/posts/new',data={'title':'Megadeth',"content":'syphony of destruction'},follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertIn('Megadeth', html)
            self.assertEqual(resp.status_code,200)


    def test_edit_form(self):
        with app.test_client() as client:
            resp=client.get(f'/posts/{self.post_id}/edit')
            html=resp.get_data(as_text=True)

            self.assertEqual(resp.status_code,200)
            self.assertIn('<p>Title: <input type="text" name="title" value="Rolling Stone"></p>',html)


    def test_post_edit(self):
        with app.test_client() as client:
            d={'title': 'edited', 'content':'new songs added'}
            resp=client.post(f'/posts/{self.post_id}/edit',data=d,follow_redirects=True)
            html=resp.get_data(as_text=True)

            self.assertEqual(resp.status_code,200)
            self.assertIn('<h3>edited</h3>',html)


#             <h3>edited</h3>

# <p>{{post.content}}</p>

