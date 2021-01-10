from django.shortcuts import render, redirect, get_object_or_404
from .models import Todolist
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
    print(tasks)
    data = {
            'tasks': tasks,
    }
    print(data)
    return render(request, 'tasks/home.html', data)

def edit(request, id):
    if request.method == "POST":
        update_task = get_object_or_404(Todolist, pk=id)
        task = request.POST["task"]
        user_name = request.POST["user_name"]
        due_date = request.POST["due_date"]
        # update_task = Todolist(task=task, user_name=user_name, due_date=due_date)
        update_task.task = task
        update_task.user_name = user_name
        update_task.due_date = due_date
        update_task.save()
        print('Saved')
        return redirect('home')
    task = get_object_or_404(Todolist, pk=id)
    data = {
        'task': task
    }
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