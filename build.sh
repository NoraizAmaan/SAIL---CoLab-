#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python Slack/manage.py collectstatic --no-input

python Slack/manage.py migrate
