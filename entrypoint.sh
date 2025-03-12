#!/bin/sh

# Ejecuta las migraciones de Alembic
alembic upgrade head

# Inicia Uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
