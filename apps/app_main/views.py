# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .models import User, Quote, Favorite
from django.contrib import messages


# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    valid = User.objects.create_user(
        request.POST['name'],
        request.POST['email'],
        request.POST['password'],
        request.POST['confirm'],
        request.POST['birthday']
    )
    if valid[0]:
        request.session['name'] = valid[1].name
        request.session['email'] = valid[1].email
        request.session['id'] = valid[1].id

        return redirect('/dashboard')
    else:
        for error in valid[1]:
            messages.add_message(request, messages.INFO, error)
    return redirect('/')

def login(request):
    valid = User.objects.login(
        request.POST['email'],
        request.POST['password']
    )

    if valid[0]:
        request.session['name'] = valid[1][0].name
        request.session['email'] = valid[1][0].email
        request.session['id'] = valid[1][0].id

        return redirect('/dashboard')
    else:
        for error in valid[1]:
            messages.add_message(request, messages.INFO, error)
        return redirect('/')

def dashboard(request):
    ctx = {
        'all_quotes': Quote.objects.all(),
        'all_usere': User.objects.all(),
        'favorite_quote': Favorite.objects.filter(user_id = request.session['id'])
    }   
    
    return render(request, 'dashboard.html', ctx)

def create(request):
    print request.POST['name'], request.POST['message']
    valid = Quote.objects.createQuote(
        request.POST['name'],
        request.POST['message'],
        request.session['id']
    )
    if valid[0]:
        return redirect('/dashboard')
    else:
        for error in valid[1]:
            messages.add_message(request, messages.INFO, error)
        return redirect('/dashboard')
    
def display(request, id):
    num = len(Quote.objects.filter(user_id=id)) #Number of quotes by the user
    ctx = {
        'user': User.objects.get(id=id),
        'quotes': Quote.objects.filter(user_id = id),
        'count': num
    }
    return render(request, 'quote.html', ctx)

def favorite(request, id):
    quote = Quote.objects.get(id=id)
    favorite_quote = Favorite.objects.create(
         user_id = request.session['id'],
         quote_id = quote.id
    )
    return redirect('/dashboard')

def remove(request, id):
    quote = Favorite.objects.get(id=id)
    quote.delete()
    return redirect('/dashboard')


def logout(request):
    request.session.delete()
    return redirect('/')