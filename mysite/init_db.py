#!/bin/env python3
import os

from django.core.management import django, call_command

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from polls.models import Word

from django.contrib.auth.models import User

# Creating superuser
if not User.objects.filter(is_superuser=True).exists():
    call_command("createsuperuser", "--noinput")
    print("Superuser created successfully.")
else:
    print("Superuser already exists.")


# Check if the database is empty
if not Word.objects.exists():
    exec(open("add_words.py").read())
else:
    print("Database already populated.")
