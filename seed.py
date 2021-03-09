"""Seed file to make sample data for db."""

from models import Post, User, db, Tag, PostTag
from app import app

# Project, EmployeeProject,

# Create all tables
db.drop_all()
db.create_all()

# Make a bunch of departments
u1 = User(first_name='Bob' , last_name='Smith' , image_url='https://upload.wikimedia.org/wikipedia/commons/a/ae/Jimi_Hendrix_1967.png')
u2 = User(first_name='Robert' , last_name='Plant' , image_url='https://upload.wikimedia.org/wikipedia/en/d/d6/Pink_Floyd_-_all_members.jpg')
u3 = User(first_name='David' , last_name='Gilmour' , image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/Battersea_Power_Station_in_London.jpg/330px-Battersea_Power_Station_in_London.jpg')

db.session.add_all([u1,u2,u3])
db.session.commit()

# # Make a bunch of employees
p1 = Post(title='jimi Hendrix', content='best artist ever',user_id=1)
p2 = Post(title='Classic rock', content='best band ever', user_id=2)
p3 = Post(title='Favorite rock music', content='classic music', user_id=3)

db.session.add_all([p1,p2,p3])
db.session.commit()

# Make a bunch of tags

t1 = Tag(name='singer')
t2 = Tag(name='rock')
t3 = Tag(name='music')

db.session.add_all([t1,t2,t3])
db.session.commit()

pt1 = PostTag(post_id=1,tag_id=1)
pt2 = PostTag(post_id=2,tag_id=2)
pt3 = PostTag(post_id=3,tag_id=3)

db.session.add_all([pt1,pt2,pt3])
db.session.commit()






