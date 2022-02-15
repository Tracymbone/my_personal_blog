from . import main
from flask import render_template, url_for, abort, request, redirect
from flask_login import login_required, current_user
from ..models import User, Post, Comment
from .. import db, photos
from .forms import UpdateForm, PostForm, CommentForm
from ..requests import get_quote


@main.route('/')
def index():
    posts = Post.query.all()
    random_quotes = get_quote()
    return render_template("index.html", posts=posts, quote=random_quotes)


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
        return redirect(url_for('.showresults'))

    return render_template('post.html', form=post_form)


@main.route('/profile/<my_name>')
@login_required
def profile(my_name):
    title = "Flask Profile"
    user = User.query.filter_by(username=my_name).first()
    if user is None:
        abort(404)

    return render_template("profile/profile.html", user=user, title=title)


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

    return render_template("profile/update.html", update_form=update_form)


@main.route('/updateImage/<my_name>', methods=['POST'])
@login_required
def u_image(my_name):
    user = User.query.filter_by(username=my_name).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic = path
        db.session.commit()
    return redirect(url_for('main.profile', my_name=my_name))


@main.route('/comment/<id>', methods=['GET', 'POST'])
@login_required
def comment(id):
    form = CommentForm()
    post = Post.query.get(id)
    fetch_all_comments = Comment.query.filter_by(post_id=id).all()
    if form.validate_on_submit():
        comment = form.comment.data
        post_id = id
        user_id = current_user._get_current_object().id
        new_comment = Comment(comment=comment, user_id=user_id, post_id=post_id)
        new_comment.save_comment()
        return redirect(url_for('.comment', id=post_id))
    return render_template('comment.html', comment_form=form, post=post, all_comments=fetch_all_comments)


@main.route('/mychanges')
def showresults():
    responses = Post.query.all()

    return render_template('show.html', all_posts=responses)


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    fetches = Post.query.get(id)
    if request.method == 'POST':
        fetches.title = request.form['title']
        fetches.category = request.form['category']
        fetches.post = request.form['post']
        db.session.commit()
        return redirect(url_for(".showresults"))

    return render_template("Modify/update.html", results=fetches)


@main.route('/delete/<id>', methods=["GET", "POST"])
def delete(id):
    data = Post.query.get(id)
    db.session.delete(data)
    db.session.commit()

    return redirect(url_for(".showresults"))
