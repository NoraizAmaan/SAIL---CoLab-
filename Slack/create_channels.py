import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Slack.settings")
django.setup()

from chat.models import Room

rooms = ['general', 'random', 'development', 'design']

for room_name in rooms:
    room, created = Room.objects.get_or_create(
        name=room_name,
        slug=room_name.lower().replace(' ', '-')
    )
    if created:
        print(f"Created room: {room_name}")
    else:
        print(f"Room already exists: {room_name}")
