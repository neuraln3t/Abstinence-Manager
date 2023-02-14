from venv import create
from django.shortcuts import render, redirect
import json
from django.utils import timezone
import datetime
from django.contrib.auth import logout as django_logout
from django.contrib.auth import login as django_login
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.conf import settings
import time
from django.db.models import Max
from django.contrib.auth.models import User

from .models import *
from .forms import *

@login_required
def index(request):
    primary_abstinence = None
    can_add = True
    ua = UserAbstinence.objects.get(user=request.user)
        
    for abst in ua.abstinences.all():
        if abst.is_primary:
            primary_abstinence = abst
    
    if primary_abstinence == None:
        absts = ua.abstinences.all()
        if len(absts) > 0:
            primary_abstinence = absts[0]
    
    if len(ua.abstinences.all()) >= settings.MAX_ABSTINENCES:
        can_add = False

    data = {
        "primary_abstinence": primary_abstinence,
        "can_add" : can_add,
    }
    return render(request, "index.html", data)

def login(request):
    args = {
            "login" : LoginForm(),
            "register" : RegisterForm()
        }

    if request.method == "POST":
        login_form = LoginForm(request.POST)
        register_form = RegisterForm(request.POST)

        if "login" in request.POST and login_form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(username=username, password=password)
            if user != None:
                if user.is_active:
                    print("Breakpoint")
                    django_login(request, user)
                else:
                    messages.error(request, "This account has been disabled!")
                    return redirect(login)
                    
            return redirect(index)
        elif "register" in request.POST and register_form.is_valid():
            username = request.POST["username"]
            email = request.POST["email"]
            password = request.POST["password"]
            user = User.objects.create_user(username=username, email=email, password=password)
            django_login(request, user)

            return redirect(index)
        else:
            return render(request, "login.html", {
                "login" : LoginForm(request.POST),
                "register" : RegisterForm(request.POST)
            })
    else:

        return render(request, "login.html", args)

@login_required
def logout(request):
    django_logout(request)

    return redirect(login)

@login_required
def abstincence_overview(request):  # Add new Abstinences, delete and edit existing ones, mark one as primary abstinence counter 
    abstinences = UserAbstinence.objects.get(user=request.user).abstinences.all()

    return render(request, "overview.html", {"abstinences" : abstinences})

@login_required
def trophies(request):  # Show earned trophies for abstinences
    abstinences = UserAbstinence.objects.get(user=request.user).abstinences.all()

    data = {
        "abstinences" : abstinences,
    }
    return render(request, "trophies.html", data)

@login_required
def check_trophies(request):
    if request.method == "POST":
        ua = UserAbstinence.objects.get(user=request.user)
        if ua.unchecked_trophies:
            ua.unchecked_trophies = False
            ua.save()

        return JsonResponse({
            "checked" : True
        })

@login_required
def history(request):
    user_history, created = History.objects.get_or_create(user=request.user)
    all_time_record = user_history.entries.aggregate(Max("count"))

    args = {
        "history" : user_history,
        "all_time_record" : all_time_record["count__max"]
    }
    print(all_time_record)
    return render(request, "history.html", args)

def new(request):
    if request.method == "POST" or request.user.is_superuser:
        print(request.POST)
        name = request.POST["name"]

        """try:
            ua = UserAbstinence.objects.get(user=request.user)
            if "is_primary" in request.POST:
                for a in ua.abstinences.all():
                    if a.is_primary:
                        a.is_primary = False
                        a.save()

        except UserAbstinence.DoesNotExist:
            ua = UserAbstinence.objects.create(user=request.user)"""

        ua = UserAbstinence.objects.get(user=request.user)

        if len(ua.abstinences.all()) >= settings.MAX_ABSTINENCES:
            
            return HttpResponse("Forbidden")
        else:
            if "is_primary" in request.POST:
                abst = Abstinence.objects.create(name=name, is_primary=True)

                for a in ua.abstinences.all():
                    if a.is_primary:
                        a.is_primary = False
                        a.save()
            else:
                abst = Abstinence.objects.create(name=name, is_primary=False)
            
            ua.abstinences.add(abst)

            return HttpResponse(json.dumps(request.POST))

def abstinence_time(request, uuid):
    abst = Abstinence.objects.get(uuid=uuid)
    pr = abst.record

    start = abst.start
    now = timezone.now()
    time = now - start

    if time > pr:
        abst.record = time + timezone.timedelta(seconds=1)
        abst.save()
    
    for trophy in Trophy.objects.all():
        if trophy not in abst.trophies.all():
            if time >= trophy.time_required:
                abst.trophies.add(trophy)
                ua = UserAbstinence.objects.get(user=request.user)
                ua.unchecked_trophies = True
                ua.save()

    time = str(time).split(".")[0]
    pr = str(pr).split(".")[0]
    
    return JsonResponse({
        "time" : time,
        "pr" : pr,
    })

def create_history_entry(request, abst):
    history, created = History.objects.get_or_create(user=request.user)

    start = abst.start
    now = timezone.now()
    time = now - start
    
    entry = HistoryEntry.objects.create(count=time, abstinence=abst)
    
    history.entries.add(entry)

def stop(request, uuid):
    if request.method == "POST":
        abst = Abstinence.objects.get(uuid=uuid)

        abst.delete()

        return JsonResponse({
            "stopped" : True
        })

def reset(request, uuid):
    if request.method == "POST":
        abst = Abstinence.objects.get(uuid=uuid)

        create_history_entry(request, abst)

        abst.start = timezone.now()
        abst.save()

        return JsonResponse({
            "reset" : True
        })

def contact(request):
    return render(request, "contact.html")

def resources(request):
    return render(request, "resources.html")

def about(request):
    return render(request, "about.html")