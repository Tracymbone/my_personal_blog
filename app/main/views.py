from . import main
from flask import render_template, url_for, abort, request, redirect
from flask_login import login_required, current_user
from ..models import User, Post, Upvote, Downvote, Comment
from .. import db, photos
from .forms import UpdateForm, PostForm, CommentForm



@main.route('/')
def index():
    # all_posts = Post.query.all()

    return render_template("index.html")

@main.route('/new-post/<id>', methods=['GET', 'POST'])
@login_required
def post(id):

    post_form = PostForm()
    if post_form.validate_on_submit():
        title = post_form.title.data
        category = post_form.category.data
        post = post_form.post.data

        new_post = Post(title=title, category=category, post=post, user=current_user)

        new_post.save_post()
        return redirect(url_for('.index'))

    return render_template('post.html', form=post_form)



@main.route('/update/<my_name>', methods=['GET', 'POST'])
@login_required
def edit_profile(my_name):
    user = User.query.filter_by(username=my_name).first()
    if user is None:
        abort(404)
    update_form = UpdateForm()
    if update_form.validate_on_submit():
        user.biography = update_form.biography.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('.profile', my_name=user.username))

    return render_template("update.html", update_form=update_form)


@main.route('/updateImage/<my_name>', methods=['POST'])
@login_required
def update_image(my_name):
    user = User.query.filter_by(username=my_name).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic = path
        db.session.commit()
    return redirect(url_for('main.profile', my_name=my_name))


