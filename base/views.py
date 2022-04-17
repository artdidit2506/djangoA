from multiprocessing import context
from pydoc_data.topics import topics
from unicodedata import name
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic
from .forms import RoomForm

# Create your views here.

# rooms = [
#     {'id': 1, 'name': 'Lets learn python'},
#     {'id': 2, 'name': 'Lets learn django'},
#     {'id': 3, 'name': 'Lets learn flask'},
# ]

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password is incorrect')
    context = {
        'base': page,
        }
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    page = 'register'
    page = UserCreationForm()
    # if request.user.is_authenticated:
    #     return redirect('home')
    
    # if request.method == 'POST':
    #     username = request.POST.get('username')
    #     email = request.POST.get('email')
    #     password = request.POST.get('password')
    #     password2 = request.POST.get('password2')
    #     if password == password2:
    #         if User.objects.filter(username=username).exists():
    #             messages.error(request, 'Username already exists')
    #             return redirect('register')
    #         else:
    #             if User.objects.filter(email=email).exists():
    #                 messages.error(request, 'Email already exists')
    #                 return redirect('register')
    #             else:
    #                 user = User.objects.create_user(username=username, email=email, password=password)
    #                 user.save()
    #                 messages.success(request, 'User created successfully')
    #                 return redirect('login')
    #     else:
    #         messages.error(request, 'Passwords do not match')
    #         return redirect('register')
    context = {
        'form': form,
    }
    return render(request, 'base/login_register.html', context)

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )
    topics = Topic.objects.all()
    room_count = rooms.count()
    context = {
        'rooms': rooms,
        'topics': topics,
        'room_count': room_count,
    }
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {
        'room': room,
    }
    return render(request, 'base/room.html', context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {
        'form': form,
    }
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    
    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')
    
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {
        'form': form,
    }
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    
    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {
        'obj': room,
    }
    return render(request, 'base/delete.html', context)