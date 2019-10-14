# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import StringField
from wtforms.validators import DataRequired, Regexp


class ImgForm(FlaskForm):
    fileimg = FileField(validators=[
        FileRequired(),
        FileAllowed(['png', 'jpg', 'jpeg', 'gif'])
    ])
    fileimg2 = FileField(validators=[
        FileRequired(),
        FileAllowed(['png', 'jpg', 'jpeg', 'gif'])
    ])


# class ImgForm2(FlaskForm):
#     fileimg2 = FileField(validators=[
#         FileRequired(),
#         FileAllowed(['png', 'jpg', 'jpeg', 'gif'])
#     ])


# class URLForm(FlaskForm):
#     txturl = StringField(validators=[
#         DataRequired(),
#         Regexp(r'(?:http\:|https\:)?\/\/.*\.(?:png|jpg|jpeg|gif)$',
#                message="Invalid image url.")
#     ])
