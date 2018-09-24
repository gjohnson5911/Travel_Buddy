# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import re
from datetime import datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    
    def login_validate(self, postData):

        errors = {}

        if len(postData['password']) <8:

            errors['password'] = "Password is not long enough"
        
        if len(postData['username']) <4:

            errors['username'] = "Username is not long enough"

        return errors


    def register_validate(self, postData):

        errors = {}

        if len(postData['name']) <4:

            errors['name'] = "Name is not long enough"

        if len(postData['username']) <4:

            errors['username'] = "Username is not long enough"
        
        if not EMAIL_REGEX.match(postData['email']):

            errors['email'] = "Email is not valid"

        if len(postData['password']) < 8:

            errors['password'] = "Password must be at least 8 char long"

        if len(postData['verify']) < 8:

            errors['verify'] = "Verify password must be at least 8 char long"

        if not postData['password'] == postData['verify']:

            errors['passwords'] = "Passwords do not match"

        return errors

class Users(models.Model):

    name = models.CharField(max_length = 255)
    username = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __repr__(self):

        return "User named {}".format(self.name)

class TripManager(models.Manager):

    def trip_validate(self, postData):

        errors = {}

        if len(postData['destination']) <1:

            errors['destination'] = "Destination cannot be empty"

        if len(postData['description']) <1:

            errors['description'] = "Description cannot be empty"

        if len(postData['travel_start']) <1:

            errors['travel_start'] = "Trip start date cannot be empty"

        if len(postData['travel_return']) <1:

            errors['trave_return'] = "Trip return date cannot be empty"

        elif datetime.strptime(postData['travel_start'], "%Y-%m-%d") <= datetime.now():

            errors['travel_start'] = "Trip must begin in the future"

        elif postData['travel_return'] <= postData['travel_start']:

            errors['travel_return'] = "Trip return date must be after start date"

        return errors

class Trips(models.Model):

    destination = models.CharField(max_length = 255)
    description = models.CharField(max_length = 255)
    creator_name = models.CharField(max_length = 255)
    start_date = models.DateField()
    return_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    users = models.ManyToManyField(Users, related_name='trips')
    objects = TripManager()

    def __repr__(self):

        return "{}'s trip to {} from {} to {}. All aboard: {}".format(self.creator_name, self.destination, self.start_date, self.return_date, self.users)



