from multiprocessing import context
from django.shortcuts import render

# Create your views here.

rooms = [
    {'id': 1, 'name': 'Lets learn python'},
    {'id': 2, 'name': 'Lets learn django'},
    {'id': 3, 'name': 'Lets learn flask'},
]

def home(request):
    context = {
        'rooms': rooms,
    }
    return render(request, 'home.html', context)

def room(request):
    return render(request, 'room.html')