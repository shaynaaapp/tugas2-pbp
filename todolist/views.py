# from urllib import response
# from django.shortcuts import render
from todolist.models import Task
# from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
# from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@login_required(login_url='/todolist/login/')
def show_todolist(request):
    data_todolist = Task.objects.filter(user=request.user)
    context = {
        'todo_list': data_todolist,
        'nama': request.user.username,
        # 'last_login': request.COOKIES['last_login'],
    }
    return render(request, "todolist.html", context)

# AJAX IMPLEMENTATION FUNCTION - Tambah Task 
@csrf_exempt
def tambah_task_ajax(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        date = datetime.datetime.now()
        is_finished = False
        data = Task.objects.create(title=title, description=description, date=date, user=request.user, is_finished=is_finished)
        # data.save()
        result = {
            'pk': data.pk,
            'fields':{
                'title': title,
                'date': date,
                'description': description,
                'is_finished': is_finished
            }
        }
        return JsonResponse(result)

@csrf_exempt
def delete_task_ajax(request, id):
    data = get_object_or_404(Task, id = id)
    data.delete()
    return HttpResponse(status=202)

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Akun telah berhasil dibuat!')
            return redirect('todolist:login')
    
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user) # melakukan login terlebih dahulu
            response = HttpResponseRedirect(reverse("todolist:show_todolist")) # membuat response
            response.set_cookie('last_login', str(datetime.datetime.now())) # membuat cookie last_login dan menambahkannya ke dalam response
            return response
        else:
            messages.info(request, 'Username atau Password salah!')
    context = {}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('todolist:login'))
    response.delete_cookie('last_login')
    return response

def tambah_task(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        date = datetime.datetime.now()
        is_finished = False
        Task.objects.create(title=title, description=description, date=date, user=request.user, is_finished=is_finished)
        response = HttpResponseRedirect(reverse('todolist:show_todolist'))
        return response
    return render(request, "taskform.html")

@csrf_exempt
def delete(request, id):
    data = get_object_or_404(Task, id = id)
    data.delete()
    return HttpResponseRedirect(reverse('todolist:show_todolist'))

def status(request, update_status):
    data_status = Task.objects.get(id=update_status)
    data_status.is_finished = True
    data_status.save()
    return HttpResponseRedirect(reverse('todolist:show_todolist'))

def show_json(request):
    data = Task.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")