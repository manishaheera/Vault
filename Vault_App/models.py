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

        if len(postData['first_name']) < 4:
            errors['username'] = "Username Must Be Atleast 4 Characters"

        if not EMAIL_REGEX.match(postData['email']):          
            errors['email'] = "EMPTY/INVALID EMAIL ADDRESS FORMAT"
        users_email = User.objects.filter(email=postData['email'])

        if len(users_email) >= 1:
            errors['email_taken'] = 'ACCOUNT WITH EMAIL ALREADY EXISTS'

        if len(postData['password']) < 8:
            errors['password'] = "PASSWORD MUST BE ATLEAST 8 CHARACTERS"
        
        if postData['password'] != postData['confirm_password']:
            errors['match_pw'] = "PASSWORD ENTRIES DO NOT MATCH"
        
        return errors


class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

