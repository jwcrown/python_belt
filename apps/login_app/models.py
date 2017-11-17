# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import bcrypt
import re

# Create your models here.


class UserManager(models.Manager):
    def validate(self, postData):
        results = {'status': True, 'errors': []}
        if len(postData['name']) < 3:
            results['errors'].append('Your name is too short.')
            results['status'] = False
        if not re.match("^[a-zA-Z ]*$", postData['name']):
            results['errors'].append('Name cannot contain numbers or special characters')
            results['status'] = False
        if not re.match("[^@]+@[^@]+\.[^@]+", postData['email']):
            results['errors'].append('Email is not valid')
            results['status'] = False
        if len(postData['password']) < 8:
            results['errors'].append('Password is too short')
            results['status'] = False
        if postData['password'] != postData['c_password']:
            results['errors'].append('Passwords do not match')
            results['status'] = False
        if len(self.filter(email = postData['email'])) > 0:
            results['errors'].append('Email entered is already registered.')
            results['status'] = False
        return results

    def creator(self, postData):
        user = self.create(name = postData['name'], email = postData['email'], password = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt()), bday = postData['bday'])
        return user

    def loginVal(self, postData):
        results = {'status': True, 'errors': [], 'user': None}
        users = self.filter(email = postData['email'])
        if len(users) < 1:
            results['status'] = False
        else:
            if bcrypt.checkpw(postData['password'].encode(), users[0].password.encode()):
                results['user'] = users[0]
            else:
                results['status'] = False
        return results
            


class User(models.Model):
    name = models.CharField(max_length =255)
    email = models.CharField(max_length =255)
    password = models.CharField(max_length =255)
    bday = models.DateField(auto_now=False, auto_now_add=False)
    objects = UserManager()