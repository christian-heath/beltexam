from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

PASSWORD_REGEX = re.compile(r'\d.*[A-Z]|[A-Z].*\d')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        if len(self.filter(email = postData['email'])) > 0:
            errors['email'] = "Email is already taken."
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email."
        if not PASSWORD_REGEX.match(postData['password']):
            errors['password'] = "Password must contain at least 1 uppercase letter and no special characters."
        if len(postData['password']) < 8:
            errors['password'] = "Password must be no fewer than 8 characters."
        if postData['password'] != postData['confirm_password']:
            errors['confirm_password'] = "Passwords do not match."
        if postData["first_name"].isalpha() != True:
            errors['first_name'] = "Invalid first name."
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be no fewer than 2 characters."
        if postData["last_name"].isalpha() != True:
            errors['last_name'] = "Invalid last name."
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be no fewer than 2 characters."
        return errors

    def login_validator(self, postData):
        errors = {}
        if len(self.filter(email = postData['email'])) < 1:
            errors['email'] = 'Email does not exist'
            return errors
        else:
            user = self.get(email = postData['email'])
            if bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                return errors
            else:
                errors['password'] = "Invalid email/password combination."
                return errors

    def create_user(self, postData):
        create = {}
        pw_hash = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
        email_hash = bcrypt.hashpw(postData['email'].encode(), bcrypt.gensalt())
        self.create(first_name = postData['first_name'], last_name=postData['last_name'], email=postData['email'], email_hash=email_hash, password=pw_hash)
        return create

class JobManager(models.Manager):
    def job_validator(self, postData):
        errors = {}
        if len(postData['title']) < 3:
            errors['title'] = "Title must be no fewer than 3 characters."
        if len(postData['title']) > 150:
            errors['title'] = "Title must be not be greater than 150 characters."
        if len(postData['desc']) < 3:
            errors['desc'] = "Description must be no fewer than 3 characters."
        if len(postData['desc']) > 150:
            errors['desc'] = "Description must be not be greater than 150 characters."
        if len(postData['location']) < 3:
            errors['location'] = "Location must be no fewer than 3 characters."
        if len(postData['location']) > 150:
            errors['location'] = "Location must be not be greater than 150 characters."
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    email_hash = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()

class Job(models.Model):
    title = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    categories = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    poster = models.ForeignKey(User, related_name="jobs_posted")
    taker = models.ForeignKey(User, related_name="jobs_taken", null=True)
    taken = models.BooleanField(default=False)

    objects = JobManager()