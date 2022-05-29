from django.shortcuts import render, redirect, get_object_or_404
from .models import Todolist
from datetime import datetime
from django.http import HttpResponseNotFound
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

import string
import random
from django.contrib.sites.shortcuts import get_current_site
# Create your views here.
def shorten_url(request, url):
    # print(request.path)
    # if request.method == "POST":
    url = url
    length = 6
    while True:
        slug = "".join(random.choices(string.ascii_uppercase, k=length))
        if Todolist.objects.filter(slug=slug).count() == 0:
            break

    shortened_url = str(get_current_site(request))+str(request.path) + slug
    print(shortened_url)
    return slug
    # data = {
    #     "domain": str(get_current_site(request))+str(request.path),
    #     "shortened_url_slug": slug
    # }
    # print(data["shortened_url_slug"])
    # return render(request, "url_shortner/url_home.html", data)
# return render(request, "url_shortner/url_home.html")

@login_required(login_url='login')
def home(request):
    if request.method == "POST":
        # print(request.POST["task"])
        task = request.POST["task"]
        due_date = request.POST["due_date"]
        url = request.POST["url"]
        slug = shorten_url(request, request.POST["url"])
        user_id = request.user
        create_task = Todolist(task=task, due_date=due_date, url=url,slug=slug, user_id=user_id)
        create_task.save()
        
        # print('Saved')
        return redirect('home')
    user_id = request.user
    tasks = Todolist.objects.filter(user_id=user_id)
    now = datetime.now(timezone.utc)
    data = {
            'tasks': tasks,
            'current_date_time': now,
            'domain': str(get_current_site(request))+str(request.path),
            # 'shortened_url_slug': slug
    }
    return render(request, 'tasks/home.html', data)

@login_required(login_url='login')
def edit(request, id):
    if request.method == "POST":
        current_user = User.objects.get(todolist__id = id)
        if current_user.id != request.user.id:
            return HttpResponseNotFound()
        update_task = get_object_or_404(Todolist, pk=id)
        task = request.POST["task"]
        user_id = request.user
        due_date = request.POST["due_date"]
        try:
            done = request.POST["done"]
            if done == "on":
                done = True
        except:
            done = False
        user_id = request.user
        update_task.task = task
        # update_task.user_name = user_name
        update_task.due_date = due_date
        update_task.user_id = user_id
        update_task.done = done
        update_task.save()
        print('Saved')
        return redirect('home')
    task = get_object_or_404(Todolist, pk=id)
    date = task.due_date.isoformat("T")[:-9]
    now = datetime.now().isoformat("T")[:-9]
    data = {
        'task': task,
        'date': date,
    }
    return render(request, 'tasks/edit.html', data)

@login_required(login_url='login')
def delete(request, id):
    current_user = User.objects.get(todolist__id = id)
    if current_user.id != request.user.id:
        return HttpResponseNotFound()
    task = get_object_or_404(Todolist, pk=id)
    if request.method == "POST":
        task.delete()
        return redirect('home')
    data = {
        'task': task
    }
    return render(request, 'tasks/delete.html', data)