#!/bin/sh
gunicorn server:app -c ./gunicorn.conf.py