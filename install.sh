#! /bin/bash

set -e

apt update && apt upgrade -y

# install pg_dump for postgres
apt install -y postgresql-client

# install s3 tools
pip install awscli

#install google cloud storage
pip install gsutil

# install poetry
pip install poetry

