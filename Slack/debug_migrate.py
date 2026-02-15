import os
import django
from django.core.management import call_command
from django.db import connection

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Slack.settings")
django.setup()

print("--- DEBUGGING MIGRATIONS ---")

# Check if chat app is installed
from django.apps import apps
if apps.is_installed('chat'):
    print("Chat app IS installed.")
else:
    print("Chat app is NOT installed.")

# Check migration status
print("\n--- Show Migrations ---")
try:
    call_command("showmigrations", "chat")
except Exception as e:
    print(f"Error showing migrations: {e}")

# Try to migrate explicitly
print("\n--- Attempting Migrate Chat 0001 ---")
try:
    call_command("migrate", "chat", "0001")
    print("Migrate command finished.")
except Exception as e:
    print(f"Migrate failed: {e}")

# Check database directly
print("\n--- Database Check ---")
with connection.cursor() as cursor:
    try:
        cursor.execute("SELECT * FROM django_migrations WHERE app='chat'")
        rows = cursor.fetchall()
        print(f"Migrations for chat in DB: {rows}")
        
        cursor.execute("SHOW TABLES LIKE 'chat_%'")
        tables = cursor.fetchall()
        print(f"Chat tables in DB: {tables}")
    except Exception as e:
        print(f"DB Error: {e}")
