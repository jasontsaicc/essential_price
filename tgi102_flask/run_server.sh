#! /bin/bash

gunicorn -c gun.conf app:app
