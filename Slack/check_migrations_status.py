import os
import django
from django.core.management import call_command
import sys

# Add the project directory to the sys.path
sys.path.append(os.getcwd())

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Slack.settings")
django.setup()

print("Checking migrations for chat app...")
try:
    call_command("showmigrations", "chat")
except Exception as e:
    print(f"Error showing migrations: {e}")
