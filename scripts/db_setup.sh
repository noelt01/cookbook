#!/bin/sh

export PGUSER="postgres"

psql -c "CREATE DATABASE recipe_db"

psql recipe_db -c "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"