import os
import django
from django.core.management import call_command

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Slack.settings")
django.setup()

print("Running makemigrations chat...")
try:
    call_command("makemigrations", "chat")
    print("makemigrations success")
except Exception as e:
    print(f"makemigrations failed: {e}")

print("Running migrate...")
try:
    call_command("migrate")
    print("migrate success")
except Exception as e:
    print(f"migrate failed: {e}")
