import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Slack.settings")
django.setup()

from chat.models import Room

with open('init_status.txt', 'w') as f:
    f.write("Starting initialization...\n")
    try:
        rooms = Room.objects.all()
        f.write(f"Found {rooms.count()} rooms.\n")
        
        default_rooms = ['general', 'random', 'development', 'design']
        for room_name in default_rooms:
            room, created = Room.objects.get_or_create(
                name=room_name,
                defaults={'slug': room_name.lower().replace(' ', '-')}
            )
            if created:
                f.write(f"Created room: {room_name}\n")
            else:
                f.write(f"Room exists: {room_name}\n")
        f.write("Finished.\n")
    except Exception as e:
        f.write(f"Error: {e}\n")
