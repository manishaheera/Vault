from django.db import models
import bcrypt
import re 

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
USERNAME_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]')

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}

        if not USERNAME_REGEX.match(postData['username']):
            errors['username'] = "Invalid Username Format"
        users_username = User.objects.filter(username=postData['username'])
        
        if len(users_username) >= 1:
            errors['username_taken'] = "Username is Taken"

        if not EMAIL_REGEX.match(postData['email']):          
            errors['email'] = "Empty/Invalid Email Format"
        users_email = User.objects.filter(email=postData['email'])

        if len(users_email) >= 1:
            errors['email_taken'] = 'Email Already In Use'

        if len(postData['password']) < 8:
            errors['password'] = "Password Must Be At Least 8 Characters"
        
        if postData['password'] != postData['confirm_password']:
            errors['match_pw'] = "Password Entries Do Not Match"
        
        return errors


class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

