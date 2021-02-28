from django.shortcuts import render, redirect, get_object_or_404
from .models import Todolist
from datetime import datetime
from django.utils import timezone
# Create your views here.
def home(request):
    if request.method == "POST":
        print(request.POST["task"])
        task = request.POST["task"]
        user_name = request.POST["user_name"]
        due_date = request.POST["due_date"]

        create_task = Todolist(task=task, user_name=user_name, due_date=due_date)
        create_task.save()
        print('Saved')
        return redirect('home')
    tasks = Todolist.objects.all()
    now = datetime.now(timezone.utc)
    print(type(tasks[1].due_date),tasks[2].due_date)
    print(type(now), now)
    # print(tasks[1].due_date > now)
    print(tasks[2].due_date < now)
    # print(tasks)
    data = {
            'tasks': tasks,
            'current_date_time': now,
    }
    # print(data)
    return render(request, 'tasks/home.html', data)

def edit(request, id):
    if request.method == "POST":
        # print(request.POST["done"])
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
        # update_task = Todolist(task=task, user_name=user_name, due_date=due_date)
        update_task.task = task
        update_task.user_name = user_name
        update_task.due_date = due_date
        update_task.done = done
        update_task.save()
        print('Saved')
        return redirect('home')
    task = get_object_or_404(Todolist, pk=id)
    date = task.due_date.isoformat("T")[:-9]
    now = datetime.now().isoformat("T")[:-9]
    print(now)
    print("task",task.due_date)
    # 1990-12-31T23:59:60Z
    print(date)
    print(now<date)
    data = {
        'task': task,
        'date': date,
    }
    print(data)
    return render(request, 'tasks/edit.html', data)

def delete(request, id):
    task = get_object_or_404(Todolist, pk=id)
    if request.method == "POST":
        task.delete()
        return redirect('home')
    data = {
        'task': task
    }
    return render(request, 'tasks/delete.html', data)