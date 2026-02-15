from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Room, Message
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.contrib import messages

def index(request):
    if not request.user.is_authenticated:
        messages.error(request, "Please login to continue or access")
        return redirect('home')
    rooms = Room.objects.all()
    if not rooms.exists():
        default_rooms = ['general', 'random', 'development', 'design']
        for room_name in default_rooms:
            Room.objects.create(name=room_name, slug=room_name.lower().replace(' ', '-'))
        rooms = Room.objects.all()
    return render(request, 'chat/index.html', {'rooms': rooms})

def room(request, slug):
    if not request.user.is_authenticated:
        messages.error(request, "Please login to continue or access")
        return redirect('home')
    rooms = Room.objects.all()
    current_room = Room.objects.get(slug=slug)
    chat_messages = Message.objects.filter(room=current_room)[0:50] # Get last 50 messages
    return render(request, 'chat/room.html', {
        'rooms': rooms,
        'current_room': current_room,
        'chat_messages': chat_messages
    })

@csrf_exempt # For simplicity in this demo, though CSRF token handling in JS is better
def upload_file(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=403)
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        file_name = default_storage.save(f"chat_uploads/{file.name}", file)
        file_url = default_storage.url(file_name)
        return JsonResponse({'file_url': file_url})
    return JsonResponse({'error': 'No file uploaded'}, status=400)

def create_room(request):
    if not request.user.is_authenticated:
        messages.error(request, "Please login to continue or access")
        return redirect('home')
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            slug = name.lower().replace(' ', '-')
            Room.objects.get_or_create(name=name, slug=slug)
            return redirect('chat_room', slug=slug)
    return redirect('chat_index')
