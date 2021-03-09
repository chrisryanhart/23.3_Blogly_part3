"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    """Creates new user"""
    __tablename__= "users"

    def __repr__(self):
        u=self
        return f"First name: {u.first_name} Last name: {u.last_name} URL: {u.image_url}"

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)

    first_name = db.Column(db.String(50),nullable=False)

    last_name = db.Column(db.String(50),nullable=False)

    image_url = db.Column(db.String(1000))

    posts = db.relationship('Post', backref='users',cascade="all, delete-orphan")

class Post(db.Model):
    __tablename__='posts'

    def __repr__(self):
        p=self
        return f'Title: {p.title} content: {p.content} created_at: {p.created_at}'

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)

    title = db.Column(db.Text,nullable=False)

    content = db.Column(db.Text, nullable=False)

    created_at=db.Column(db.DateTime, nullable=False, default=datetime.now())

    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)

    # user_details = db.relationship('User', backref='posts')

    post_tags = db.relationship('PostTag',backref='posts')


class Tag(db.Model):

    __tablename__ = 'tags'

    def __repr__(self):
        t=self
        return f'Tag: {t.name}'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.Text, unique=True)

    # use 'through' relationship b/t Tag & Post
    posts = db.relationship('Post', secondary='posts_tags', backref='tags')

class PostTag(db.Model):

    __tablename__='posts_tags'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)

    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)