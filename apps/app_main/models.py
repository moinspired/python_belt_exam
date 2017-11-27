# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import bcrypt 
from datetime import datetime

now = str(datetime.now())


def validateEmail( email ):
    try:
        validate_email( email )
        return True
    except ValidationError:
        return False

class UserManager(models.Manager):
   
    def create_user(self, name, email, password, confirm, birthday):
        print name, email, password, birthday, confirm
        errors = []
        if len(name) < 3:
            errors.append("Name should be more than one characters")
        if len(email) < 3:
            errors.append("email can not be empty")
        elif len(User.objects.filter(email=email)) > 0:
            errors.append("Email already exits")
        elif not validateEmail(email):
            errors.append("Email must be valid")
        if len(password) < 5:
            errors.append("Password must be at least 5 characters")
        if password != confirm:
            errors.append("Password must match confirm password")
        if birthday > now:
            errors.append("Date can not be in the future")

        if len(errors) > 0:
            return (False, errors)
        else:
            
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            user = User.objects.create(name = name, email = email, pw_hash=pw_hash, birthday=birthday)
            return (True, user)
        
    def login(self, email, password):
        errors = []
        user = User.objects.filter(email=email)
        if len(email) < 3:
            errors.append("email can not be empty")
        elif not validateEmail(email):
            errors.append("Email must be valid")
        elif len(user) == 0:
            errors.append("Email does not exist")
        if len(password) < 5:
            errors.append("Password must be at least 5 characters")
        if len(errors) > 0:
            print errors
            return (False, errors)
        else:
            if bcrypt.checkpw(password.encode(), user[0].pw_hash.encode()):
                return (True, user)
            else:
                return (False, ["Incorrect Password!"])

class QuoteManager(models.Manager):
    def createQuote(self, name, message, id):
        print name, message
        errors = []
        
        if len(name) < 3:
                errors.append("Name should be more than one characters")
        if len(message) < 3:
            errors.append("Message can not be empty. And must be at least a sentence long.")

        if len(errors) > 0:
            return (False, errors)
        else:
            quote = Quote.objects.create(name=name, message=message, user_id=id )
            return (True, quote)

class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    pw_hash = models.CharField(max_length=255)
    birthday =  models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class Quote(models.Model):
    name = models.CharField(max_length=255)
    message = models.TextField()
    user = models.ForeignKey(User, related_name="quote")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
  
    objects = QuoteManager()

class Favorite(models.Model):
    user = models.ForeignKey(User, related_name="fivoite_quote")
    quote = models.ForeignKey(Quote, related_name="fivoite_quote")
  
    
