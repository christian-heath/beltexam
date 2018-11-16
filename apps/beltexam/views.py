from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    if 'authenticator' not in request.session:
        return render(request, 'beltexam/index.html')
    else:
        return redirect('/dashboard')

def dashboard(request):
    if 'authenticator' not in request.session:
        return render(request, 'beltexam/hacker.html')
    else:
        context = {
            'user': User.objects.get(email_hash=request.session['authenticator']),
            'jobs': Job.objects.all(),
            'user_jobs': User.objects.get(email_hash=request.session['authenticator']).jobs_taken.all()
        }
        return render(request, 'beltexam/dashboard.html', context)

def hacker(request):
    return render(request, 'beltexam/hacker.html')

def new(request):
    if 'authenticator' not in request.session:
        return render(request, 'beltexam/hacker.html')
    else:
        context = {
            'user': User.objects.get(email_hash=request.session['authenticator'])
        }
        return render(request, 'beltexam/new.html', context)

def edit(request, id):
    if 'authenticator' not in request.session:
        return render(request, 'beltexam/hacker.html')
    else:
        context = {
            'user': User.objects.get(email_hash=request.session['authenticator']),
            'job': Job.objects.get(id=id)
        }
        return render(request, 'beltexam/edit.html', context)

def show(request, id):
    if 'authenticator' not in request.session:
        return render(request, 'beltexam/hacker.html')
    else:
        context = {
            'user': User.objects.get(email_hash=request.session['authenticator']),
            'job': Job.objects.get(id=id)
        }
        return render(request, 'beltexam/show.html', context)

def register(request):
    if request.method == 'POST':
        errors = User.objects.registration_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags='register')
            return redirect('/')
        else:
            create = User.objects.create_user(request.POST)
            messages.success(request, "User successfully created!")
            user = User.objects.last()
            request.session['authenticator'] = user.email_hash
            request.session['user_id'] = user.id
        return redirect('/dashboard')    
    else:
        return redirect('/')

def login(request):
    if request.method == 'POST':
        errors = User.objects.login_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags='login')
            return redirect('/')
        else:
            user = User.objects.get(email = request.POST['email'])
            request.session['authenticator'] = user.email_hash
            request.session['user_id'] = user.id
        return redirect('/dashboard')    
    else:
        return redirect('/')

def logout(request):
    
    if request.method == 'POST':
        request.session.clear()
        return redirect('/')
    else:
        return redirect('/')

def new_job(request):
    if 'authenticator' not in request.session:
        return render(request, 'beltexam/hacker.html')
    if request.method == 'POST':
        errors = Job.objects.job_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/new')
        else:
            Job.objects.create(title=request.POST['title'], desc=request.POST['desc'], location=request.POST['location'], categories=request.POST['category'], poster=User.objects.get(id=request.POST['user_id']))
            return redirect('/dashboard')
    else:
        return redirect('/')

def add(request):
    if 'authenticator' not in request.session:
        return render(request, 'beltexam/hacker.html')
    if request.method == 'POST':
        job = Job.objects.get(id=request.POST['job_id'])
        job.taker = User.objects.get(id=request.POST['user_id'])
        job.taken = True
        job.save()
        return redirect('/dashboard')
    else:
        return redirect('/')

def update(request, id):
    if 'authenticator' not in request.session:
        return render(request, 'beltexam/hacker.html')
    if request.method == 'POST':
        if request.POST['poster_id'] != request.POST['user_id']:
            messages.error(request, "You do not have permission to edit this job. Users may only edit jobs if they are the original poster.")
            return redirect('/edit/'+id)
        errors = Job.objects.job_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
                return redirect('/edit/'+id)
        else:
            job = Job.objects.get(id= id)
            job.title = request.POST['title']
            job.desc = request.POST['desc']
            job.location = request.POST['location']
            job.save()
            return redirect('/dashboard')    
    else:
        return redirect('/')

def give_up(request):
    if 'authenticator' not in request.session:
        return render(request, 'beltexam/hacker.html')
    if request.method == 'POST':
        job = Job.objects.get(id=request.POST['job_id'])
        job.taken = False
        job.save()
        return redirect('/dashboard')
    else:
        return redirect('/')

def delete(request):
    if 'authenticator' not in request.session:
        return render(request, 'beltexam/hacker.html')
    if request.method == 'POST':
        job = Job.objects.get(id=request.POST['job_id'])
        job.delete()
        return redirect('/dashboard')
    else:
        return redirect('/')