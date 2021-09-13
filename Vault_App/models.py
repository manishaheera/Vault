from django.db import models
import bcrypt
import re 

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
USERNAME_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]')

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}

        if not USERNAME_REGEX.match(postData['username']):
            errors['username'] = "Please enter a valid username."
        users_username = User.objects.filter(username=postData['username'])
        
        if len(users_username) >= 1:
            errors['username_taken'] = "This username is already taken."

        if not EMAIL_REGEX.match(postData['email']):          
            errors['email'] = "Please enter a valid email address."
        users_email = User.objects.filter(email=postData['email'])

        if len(users_email) >= 1:
            errors['email_taken'] = 'A user with this email already exists.'

        if len(postData['password']) < 8:
            errors['password'] = "Password must Be at least 8 characters."
        
        if postData['password'] != postData['confirm_password']:
            errors['match_pw'] = "Passwords do not match. Please try again."
        
        return errors


class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

