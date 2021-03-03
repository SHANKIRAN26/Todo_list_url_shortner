from django.shortcuts import render, redirect, get_object_or_404
from .models import Todolist
from datetime import datetime
from django.http import HttpResponseNotFound
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def home(request):
    if request.method == "POST":
        print(request.POST["task"])
        task = request.POST["task"]
        due_date = request.POST["due_date"]
        user_id = request.user
        create_task = Todolist(task=task, due_date=due_date, user_id=user_id)
        create_task.save()
        print('Saved')
        return redirect('home')
    user_id = request.user
    tasks = Todolist.objects.filter(user_id=user_id)
    now = datetime.now(timezone.utc)
    data = {
            'tasks': tasks,
            'current_date_time': now,
    }
    return render(request, 'tasks/home.html', data)

@login_required(login_url='login')
def edit(request, id):
    if request.method == "POST":
        update_task = get_object_or_404(Todolist, pk=id)
        task = request.POST["task"]
        user_name = request.POST["user_name"]
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
    current_user = User.objects.get(todolist__id = id)
    if current_user.id != request.user.id:
        return HttpResponseNotFound()
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
    task = get_object_or_404(Todolist, pk=id)
    if request.method == "POST":
        task.delete()
        return redirect('home')
    current_user = User.objects.get(todolist__id = id)
    if current_user.id != request.user.id:
        return HttpResponseNotFound()
    data = {
        'task': task
    }
    return render(request, 'tasks/delete.html', data)