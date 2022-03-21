#!/bin/sh
uvicorn app.main --bind=0.0.0.0:80 --timeout 120
