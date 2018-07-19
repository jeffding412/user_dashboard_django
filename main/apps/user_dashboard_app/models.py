from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['email']) < 1:
            errors["email"] = "User email is a required field"
        elif not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "User email is not in valid format"

        if len(postData['first']) < 2:
            errors["first"] = "User first name should be at least 2 characters"
        elif not re.match(r"^[a-zA-Z]+$", postData['first']):
            errors["first"] = "User first name can only contain letters"

        if len(postData['last']) < 2:
            errors["last"] = "User last name should be at least 2 characters"
        elif not re.match(r"^[a-zA-Z]+$", postData['first']):
            errors["last"] = "User last name can only contain letters"

        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        elif postData['password'] != postData['confirm']:
            errors["confirm"] = "Passwords do not match"

        return errors

    def login_validator(self, postData):
        errors = {}
        user = User.objects.filter(email=postData['email'])
        if not user:
            errors['failure'] = "No email/password combo"
        elif not bcrypt.checkpw(postData['password'].encode(), user[0].password_hash.encode()):
            errors['failure'] = "No email/password combo"
        
        return errors

    def edit_info_validator(self, postData):
        errors = {}
        if len(postData['email']) < 1:
            errors["email"] = "User email is a required field"
        elif not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "User email is not in valid format"

        if len(postData['first']) < 2:
            errors["first"] = "User first name should be at least 2 characters"
        elif not re.match(r"^[a-zA-Z]+$", postData['first']):
            errors["first"] = "User first name can only contain letters"

        if len(postData['last']) < 2:
            errors["last"] = "User last name should be at least 2 characters"
        elif not re.match(r"^[a-zA-Z]+$", postData['first']):
            errors["last"] = "User last name can only contain letters"

        return errors

    def change_password_validator(self, postData):
        errors = {}
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        elif postData['password'] != postData['confirm']:
            errors["confirm"] = "Passwords do not match"
        
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password_hash = models.CharField(max_length=255)
    user_level = models.IntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class Post(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    poster = models.ForeignKey(User, related_name="posts")
    receiver = models.ForeignKey(User, related_name="wall_posts")

class Comment(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    display_time = models.DateTimeField(auto_now=True)
    commenter = models.ForeignKey(User, related_name="comments")
    post = models.ForeignKey(Post, related_name="replies")