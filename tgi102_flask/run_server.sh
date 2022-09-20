#! /bin/bash

gunicorn -c gun.py app:app
