#!/bin/bash
source venv/bin/activate
gunicorn --bind 0.0.0.0:9891 --workers 10 wsgi:app
