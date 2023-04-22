#!/bin/sh
docker build -t pg-backup .
docker image tag pg-backup:latest simple2b/pg-backup
docker image push simple2b/pg-backup
