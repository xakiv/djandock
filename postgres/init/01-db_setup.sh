#!/bin/sh

export PGUSER="$POSTGRES_USER"

psql -d $POSTGRES_DB -c "CREATE SCHEMA IF NOT EXISTS switch AUTHORIZATION $POSTGRES_USER"
