from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Todo
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse

# Create your views here.
def homepage(request):
    return render(request, "home.html")

def signup(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get('password')
        confirmpassword = request.POST.get("confirmpassword")
        if password == confirmpassword:
            User.objects.create_user(
                username=username,
                password=password,
                last_name=last_name, first_name=first_name, email=email)
            messages.success(request, "Account created successfully! You can now login.")
        else:
            messages.error(request, "Passwords do not match. Please try again.")
    return render(request, "signup.html")

def signin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('create_and_list_todo')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    return render(request, "signin.html")

# @login_required
# def create_and_list_todo(request):
#     if request.method == 'POST':
#         if 'search' in request.POST:
#             query = request.POST.get('search')
#             tasks = Todo.objects.filter(u_id=request.user, taskname__icontains=query)
#             return render(request, 'task_list.html', {'tasks': tasks})
#         else:
#             taskname = request.POST.get('taskname')
#             date = request.POST.get('date')
#             status = request.POST.get('status')
#             if status:
#                 status = 'started'
#             else:
#                 status = 'in progress'
#             # Check if a task with the same name already exists for the user
#             if Todo.objects.filter(u_id=request.user, taskname=taskname).exists():
#                 messages.error(request, 'A task with this name already exists.')
#             else:
#                 Todo.objects.create(taskname=taskname, date=date, status=status, u_id=request.user)
#                 messages.success(request, 'Task created successfully!')
#             return redirect('create_and_list_todo')  # Redirect to the same page to avoid resubmission
#     tasks = Todo.objects.filter(u_id=request.user, status='in progress')
#     return render(request, 'task_list.html', {'tasks': tasks})

# def edit_todo(request, pk):
#     todo_item = Todo.objects.get(pk=pk)
#     if request.method == 'POST':
#         taskname = request.POST.get('taskname')
#         date = request.POST.get('date')
#         status = request.POST.get('status')
#         if status:
#             status = 'started'
#         else:
#             status = 'in progress'
#         todo_item.taskname = taskname
#         todo_item.date = date
#         todo_item.status = status
#         todo_item.save()
#         messages.success(request, 'Todo item updated successfully!')
#         return redirect('create_and_list_todo')
#     return render(request, 'update_task.html', {'todo_item': todo_item})
# from django.contrib import messages

@login_required
def create_and_list_todo(request):
    if request.method == 'POST':
        if 'search' in request.POST:
            query = request.POST.get('search')
            tasks = Todo.objects.filter(u_id=request.user, taskname__iexact=query)
            return render(request, 'task_list.html', {'tasks': tasks})
        else:
            taskname = request.POST.get('taskname')
            date = request.POST.get('date')
            status = request.POST.get('status')
            if status:
                status = 'started'
            else:
                status = 'in progress'
            # Check if a task with the same name already exists for the user
            if Todo.objects.filter(u_id=request.user, taskname__iexact=taskname).exists():
                messages.error(request, 'A task with this name already exists.')
            else:
                Todo.objects.create(taskname=taskname, date=date, status=status, u_id=request.user)
                messages.success(request, 'Task created successfully!')
            return redirect('create_and_list_todo')  # Redirect to the same page to avoid resubmission
    tasks = Todo.objects.filter(u_id=request.user, status='in progress')
    return render(request, 'task_list.html', {'tasks': tasks})


def edit_todo(request, pk):
    todo_item = Todo.objects.get(pk=pk)
    if request.method == 'POST':
        taskname = request.POST.get('taskname')
        date = request.POST.get('date')
        status = request.POST.get('status')
        if status:
            status = 'started'
            # messages.info(request, 'Todo item marked as started!')
        else:
            status = 'in progress'
        todo_item.taskname = taskname
        todo_item.date = date
        todo_item.status = status
        todo_item.save()
        if status == 'started':
            messages.info(request, 'Todo item marked as started!')
        else:
            messages.success(request, 'Todo item updated successfully!')
        return redirect('create_and_list_todo')
    return render(request, 'update_task.html', {'todo_item': todo_item})

def delete_todo(request, pk):
    todo_item = Todo.objects.get(pk=pk)
    todo_item.delete()
    messages.set_level(request, messages.DEBUG)
    messages.debug(request, 'Todo item deleted successfully!')
    return redirect('create_and_list_todo')
def finish(request, id):
    v = Todo.objects.get(id=id)
    v.status = 'completed'
    v.save()
    messages.success(request, "Task completed successfully!")
    return redirect('create_and_list_todo')

@login_required
def finding(request, status=None):
    if status is None:
        all_todos = Todo.objects.filter(u_id=request.user)
    elif status == 'started':
        all_todos = Todo.objects.filter(u_id=request.user, status='started')
    elif status == 'in_progress':
        all_todos = Todo.objects.filter(u_id=request.user, status='in progress')
    elif status == 'completed':
        all_todos = Todo.objects.filter(u_id=request.user, status='completed')
    else:
        all_todos = Todo.objects.filter(u_id=request.user)
    return render(request, "task_list.html", {"tasks": all_todos, "status": status})

def signout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('signin')

# def create_and_list_todo(request):
#     if request.method == 'POST':
#         taskname = request.POST.get('taskname')
#         date = request.POST.get('date')
#         status = request.POST.get('status') == 'on' # Convert 'on' to True, otherwise False
#         todo.objects.create(taskname=taskname, date=date, status=status, u_id=request.user)
#         messages.success(request, 'Todo created successfully!')
#         return redirect('create_and_list_todo') # Redirect to the same page to avoid resubmission
#     tasks = todo.objects.filter(u_id=request.user,status=0)
#     return render(request, 'task_list.html', {'tasks': tasks})

