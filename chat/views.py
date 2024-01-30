from django.shortcuts import render,redirect

from chat.models import Room
from django.contrib.auth.models import AnonymousUser,User

def index_view(request):
    user = request.user
    if str(user) == 'AnonymousUser':
        return redirect('login')
    return render(request, 'index.html', {
        'rooms': Room.objects.all(),
    })
def room_view(request, room_name):
    user = request.user
    print(user)
    if str(user) == 'AnonymousUser':
        return redirect('login')
    chat_room, created = Room.objects.get_or_create(name=room_name)
    return render(request, 'room.html', {
        'room': chat_room,
    })

