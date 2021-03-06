from flask_login import UserMixin
from . import db, login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    category = db.Column(db.String)
    post = db.Column(db.String(255))
    posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    comment = db.relationship('Comment',backref='new',lazy='dynamic')


    def save_post(self):
        db.session.add(self)
        db.session.commit()


class User(UserMixin,db.Model):
    __tablename__="users"
    id=db.Column(db.Integer(),primary_key=True)
    username=db.Column(db.String(255),index=True)
    email=db.Column(db.String(255),index=True)
    biography=db.Column(db.String(255))
    profile_pic=db.Column(db.String())
    password_secure=db.Column(db.String(255))
    posts= db.relationship('Post',backref = 'user',lazy ="dynamic")
    comment = db.relationship('Comment',backref='user',lazy='dynamic')


    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.password_secure = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_secure, password)

    def __repr__(self):
        return f'User: {self.username}'

@login_manager.user_loader
def load_user(user_id):
    """call back function that retrieves a user when a unique identifier is passed"""
    return User.query.get(int(user_id))

def __repr__(self):
    return f'User: {self.name}'



class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls, post_id):
        comments_results = Comment.query.filter_by(post_id=post_id).all()

        return comments_results

    def __repr__(self):
        return f'comment:{self.comment}'


