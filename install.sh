#! /bin/bash

set -e

apt update && apt upgrade -y

# install pg_dump for postgres
apt install -y postgresql-client

# install poetry
pip install poetry

