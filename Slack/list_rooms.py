import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Slack.settings")
django.setup()

from chat.models import Room

print("Checking for existing rooms...")
rooms = Room.objects.all()
print(f"Found {rooms.count()} rooms.")
for room in rooms:
    print(f"- {room.name} ({room.slug})")

if rooms.count() == 0:
    print("Database is empty. Attempting to create rooms again...")
    default_rooms = ['general', 'random', 'development', 'design']
    for room_name in default_rooms:
        Room.objects.create(name=room_name, slug=room_name.lower().replace(' ', '-'))
    print("Rooms created.")
