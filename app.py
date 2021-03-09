"""Blogly application."""
from flask import Flask, render_template, request, redirect
from models import db, connect_db, User, Post, Tag, PostTag

from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_part2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def go_home():
    return render_template('welcome.html')


@app.route('/users')
def show_all_users():
    """Add code to get all users from db.  
    -make each user a link to /users/id
    -have link to add user
    Show all users"""

    users = User.query.all()

    return render_template('allUsers.html',users=users)


@app.route('/users/new')
def make_new_user():
    """
    Show form for adding a user
    """

    return render_template('newUser.html')

@app.route('/users/new', methods=['POST'])
def post_new_user():
    """Add user to db"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    new_user = User(first_name=first_name,last_name=last_name,image_url=image_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>')
def show_user_info(user_id):
    """Show infor about given user
    -have button to edit/delete user
    """
    user = User.query.get(user_id)
    posts = user.posts

    return render_template('userInfo.html', user=user, posts=posts)



@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    """Show user edit page
    -have save/cancel button
    """
    unique_user = User.query.get(user_id)

    return render_template('editUser.html',user=unique_user)

# <int:user_id>

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def process_edit(user_id):
    """Process the edit form"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    user = User.query.get(user_id)



    db.session.add(user)
    db.session.commit()

    # make if statement to test for form value presence


    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')





# Part 2 blog post routes

@app.route('/users/<int:user_id>/posts/new')
def new_post_form(user_id):
    user = User.query.get(user_id)
    # posts = user.posts

    tags = Tag.query.all()
    return render_template('newPostForm.html', user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def submit_post(user_id):
    # add post to submit to postgres

    title = request.form['title']
    content = request.form['content']

    # check for differences with jinja template
    tag_ids = [int(num) for num in request.form.getlist('check')]
    tag_objs = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    # tags = request.form.getlist('check')

    new_post = Post(title=title, content=content, user_id=user_id, tags=tag_objs)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):

    post = Post.query.get(post_id)
    user = post.users
    tags = post.tags

    return render_template('displayPost.html',post=post,user=user, tags=tags)

@app.route('/posts/<int:post_id>/edit')
def edit_form(post_id):
    tag_arr=[]

    post = Post.query.get(post_id)
    tags = Tag.query.all()
    selected_tags = post.tags

    for tag in selected_tags:
        tag_arr.append(tag.name)


    return render_template('editPost.html',post=post,tags=tags,tag_arr=tag_arr)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def post_edit(post_id):

    title = request.form['title']
    content = request.form['content']
    tags = request.form.getlist('check')

    post = Post.query.get(post_id)

    post.title = title
    post.content = content

    tag_ids = [int(num) for num in request.form.getlist('check')]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    test=1

    db.session.add(post)
    db.session.commit()
    
    # find PostTags to delete
    # items = PostTag.query.filter_by(post_id=1).all()

    # for item in items:
    #     db.session.delete(item)
    
    # db.session.commit()

    # # add in new tags
    # for tag in tags:
    #     new_tag = Tag.query.filter_by(name=tag).all()
    #     new_postTag = PostTag(post_id=post_id, tag_id=new_tag[0].id)

    #     db.session.add(new_postTag)
    
    # db.session.commit()

    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    
    post = Post.query.get(post_id)
    user_id = post.users.id

    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')


# Part 3 Tag routes

@app.route('/tags')
def list_tags():
    tags = Tag.query.all()
    return render_template('allTags.html',tags=tags)


@app.route('/tags/<int:tag_id>')
def tag_detail(tag_id):
    tag = Tag.query.get(tag_id)
    posts = tag.posts
    return render_template('tagDetail.html',tag=tag, posts=posts,tag_id=tag_id)

@app.route('/tags/new')
def add_tag():

    return render_template('addTag.html')

@app.route('/tags/new', methods=['POST'])
def new_tag_form():

    tag = request.form['tag']

    new_tag = Tag(name=tag)

    db.session.add(new_tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def edit_tag_form(tag_id):
    tag = Tag.query.get(tag_id)


    return render_template('editTag.html',tag=tag, tag_id=tag_id)

@app.route('/tags/<int:tag_id>/edit',methods=['POST'])
def process_tag_edit(tag_id):
    name = request.form['name']
    tag = Tag.query.get(tag_id)

    tag.name = name

    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    tag = Tag.query.get(tag_id)

    db.session.delete(tag)
    db.session.commit()

    return redirect('/tags')

