#!/bin/bash

celery worker -A server.worker.worker --loglevel=info