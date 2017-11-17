# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from ..login_app.models import User
from django.db import models
import re

# Create your models here.
class AptManager(models.Manager):
    def create_apt(self, postData, user_id):
        new_apt = self.create(date = postData['date'], time = postData['time'], task = postData['task'], status = 'pending', user_apt = User.objects.get(id = user_id))
        return new_apt

    def validate(self, postData):
        results = {'status': True, 'errors': []}
        if len(postData['task']) < 1:
            results['errors'].append('Task field cannot be empty')
            results['status'] = False
        return results
        
class Apt(models.Model):
    task = models.CharField(max_length =255)
    status = models.CharField(max_length =255)
    date = models.CharField(max_length =255)
    time = models.TimeField(auto_now=False, auto_now_add=False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    user_apt = models.ForeignKey(User, related_name="apts")
    objects = AptManager()