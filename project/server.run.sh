#!/bin/bash

gunicorn -w 1 -b 0.0.0.0:8080 --log-level=debug --reload server.wsgi