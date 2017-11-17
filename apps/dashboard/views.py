# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
import datetime
from django.contrib import messages
from ..login_app.models import User
from models import Apt


# Create your views here.
def index(request):
    if 'email' not in request.session:
        return redirect('/')
    user_id = request.session['id']
    now = datetime.datetime.now()
    request.session['now'] = str(now.strftime("%Y-%m-%d"))
    today_apt = {
        "today": Apt.objects.filter(user_apt = user_id).order_by('date', 'time')
    }
    
    return render(request, 'dashboard/index.html', today_apt)

def add(request):
    user_id = request.session['id']
    results = Apt.objects.validate(request.POST)
    if results['status'] == True:
        new_apt = Apt.objects.create_apt(request.POST, user_id)
        messages.success(request, 'New appointment has been created!')
    else:
        for error in results['errors']:
            messages.error(request, error)
    
    return redirect('/dashboard')

def delete(request, id):
    user_id = request.session['id']
    delete = Apt.objects.filter(id = id).delete()
    return redirect('/dashboard')

def edit(request, apt_id):
    if 'email' not in request.session:
        return redirect('/')
    default_apt = {
        "default": Apt.objects.filter(id = apt_id)
    }
    request.session['apt'] = apt_id
    return render(request, 'dashboard/edit.html', default_apt)

def update(request, apt_id):
    results = Apt.objects.validate(request.POST)
    if results['status'] == True:
        edit_apt = Apt.objects.get(id = apt_id)
        edit_apt.task = request.POST['task']
        edit_apt.status = request.POST['status']
        edit_apt.date = request.POST['date']
        edit_apt.time = request.POST['time']
        edit_apt.save()
        messages.success(request, 'Appointment has been updated!')
        return redirect('/dashboard')
    else:
        for error in results['errors']:
            messages.error(request, error)
    return redirect('/dashboard/{}/edit'.format(apt_id))