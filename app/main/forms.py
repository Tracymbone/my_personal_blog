from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField, SelectField,PasswordField
from wtforms.validators import input_required
categories = ['lifestyle','food','fashion','hobbies']


class UpdateForm(FlaskForm):
    biography = TextAreaField("Your Biography", validators=[input_required(message='Biography field is required')],render_kw={"placeholder": "Your Biography"})
    submit = SubmitField("Update Profile")


class PostForm(FlaskForm):
    title = StringField("post title", validators=[input_required(message='post title is required')],render_kw={ "placeholder" : "post Title"})
    category = SelectField("post category", validators=[input_required(message="post Category required")],choices=categories)
    post = TextAreaField("post description", validators=[input_required(message="post required")],render_kw={ "placeholder" :"post description"})
    submit = SubmitField("Post post")


class CommentForm(FlaskForm):
    comment = TextAreaField('post comment', validators=[input_required(message="Comment field is required")],render_kw={"placeholder": "Your Comment"})
    submit = SubmitField('Comment')