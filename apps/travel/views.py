# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from datetime import datetime
from .models import Users, Trips
import bcrypt

#render login/registration page
def index(request):
    #log out any previous user
    if 'user_id' in request.session:
        request.session['user_id'] = None

    return render(request, 'travel/login_reg.html')

#validate login credentials, then log in user if correct. Redirect to /travels
def login(request):

    #validation
    errors = Users.objects.login_validate(request.POST)

    if len(errors):
        
        for tag, error in errors.iteritems():
           
           messages.error(request, error, extra_tags=tag)
        
        return redirect('/main')

    #if info entry is valid 
    else:

        username = request.POST['username']
        test_pass = request.POST['password']
        #check that a user exists with that username
        try_user = Users.objects.filter(username = username)
        #if the username exists
        if len(try_user)>0:
            real_pass = try_user[0].password
            #check password against password in DB
            if bcrypt.checkpw(test_pass.encode(), real_pass.encode()):
                #set session and redirect to /travels
                request.session['user_id'] = try_user[0].id
                return redirect('/travels')
            else: #if password doesn't match
                messages.error(request, "Password was not correct")
                return redirect('/main')
        else: #if username wasn't found
            messages.error(request, "Username was not correct")
            return redirect('/main')
            
#validate user info, then create new user with that info. Redirect to /travels
def register(request):
    #validate
    errors = Users.objects.register_validate(request.POST)

    if len(errors):
        
        for tag, error in errors.iteritems():
           
            messages.error(request, error, extra_tags=tag)
        
        return redirect('/main')
    
    #if info is valid
    else:
        
        name = request.POST['name']
        username = request.POST['username']
        email = request.POST['email']
        password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())

        #check that username isn't already taken
        try_user = Users.objects.filter(username = username)
        if len(try_user) > 0:

            messages.error(request, "Username is taken")
            return redirect('/main')

        #if username is available, create user in DB and start session
        else:
        
            Users.objects.create(name = name, username = username, email = email, password = password)
            new_user = Users.objects.get(email = email)
            request.session['user_id'] = new_user.id
            
            return redirect('/travels')

#render home page, passing user info, user's travel plans and other user's travel plans
def home(request):
    #get current user
    user = Users.objects.get(id = request.session['user_id'])

    #get user's travel plans
    user_plans = Trips.objects.filter(creator_name = user.name,)
    joined_plans = Trips.objects.filter(users = user)

    #get all travel plans, excluding the current user's
    other_plans = Trips.objects.exclude(creator_name = user.name)

    filter_plans = []
    for plan in other_plans:
        if len(plan.users.all()) <1:
            filter_plans.append(plan)
        else:
            for acnt in plan.users.all():
                if not acnt == user:
                    filter_plans.append(plan)
                    break
    context = {
        'user': user,
        'user_plans': user_plans,
        'joined_plans': joined_plans,
        'other_plans': filter_plans
    }
    return render(request, 'travel/home.html', context)

    #Render a page showing details on one specific trip. Pass trip object and any other users joining the trip, excepting the creator
def display_trip(request, trip_id):
    #get trip object
    trip = Trips.objects.get(id = trip_id)

    #get list of all users on the trip, excluding the current user
    trip_users = trip.users.all()

    context = {
        'trip': trip,
        'trip_users': trip_users
    }

    return render(request, 'travel/trip.html', context)
     
#render a page showing a form for creating a new trip
def add(request):

    return render(request, 'travel/new_plan.html')

#validate trip info, then create new object and redirect to /main
def new_travel(request):

    #validate info entry
    errors = Trips.objects.trip_validate(request.POST)
    print errors
    if len(errors):
        
        for tag, error in errors.iteritems():
           
            messages.error(request, error, extra_tags=tag)
        
        return redirect('/travels/add')

    #if info entry is valid 
    else:

        destination = request.POST['destination']
        description = request.POST['description']
        travel_start = datetime.strptime(request.POST['travel_start'], "%Y-%m-%d")
        travel_return = datetime.strptime(request.POST['travel_return'], "%Y-%m-%d")
        creator = Users.objects.get(id = request.session['user_id'])

        Trips.objects.create(destination = destination, description = description, creator_name = creator.name, start_date = travel_start, return_date = travel_return)

        return redirect('/travels')

#add current user to the specified trip, return to /travels
def add_to_trip(request, trip_id):

    #get trip
    trip = Trips.objects.get(id = trip_id)
    
    #get user
    user = Users.objects.get(id = request.session['user_id'])

    #add user to trip's users
    trip.users.add(user)

    return redirect('/travels')