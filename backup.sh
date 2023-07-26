#! /bin/sh

set -e
set -o pipefail

echo S3_BUCKET=${S3_BUCKET}
if [ "${S3_BUCKET}" = "**None**" ]; then
  METHOD=FS
else
  METHOD=S3
fi
echo METHOD=${METHOD}

if [ "${METHOD}" = "S3" ] && [ "${S3_ACCESS_KEY_ID}" = "**None**" ]; then
  echo "You need to set the S3_ACCESS_KEY_ID environment variable."
  exit 1
fi

if [ "${METHOD}" = "S3" ] && [ "${S3_SECRET_ACCESS_KEY}" = "**None**" ]; then
  echo "You need to set the S3_SECRET_ACCESS_KEY environment variable."
  exit 1
fi


if [ "${POSTGRES_DATABASE}" = "**None**" ]; then
  echo "You need to set the POSTGRES_DATABASE environment variable."
  exit 1
fi

if [ "${POSTGRES_HOST}" = "**None**" ]; then
  if [ -n "${POSTGRES_PORT_5432_TCP_ADDR}" ]; then
    POSTGRES_HOST=$POSTGRES_PORT_5432_TCP_ADDR
    POSTGRES_PORT=$POSTGRES_PORT_5432_TCP_PORT
  else
    echo "You need to set the POSTGRES_HOST environment variable."
    exit 1
  fi
fi

if [ "${POSTGRES_USER}" = "**None**" ]; then
  echo "You need to set the POSTGRES_USER environment variable."
  exit 1
fi

if [ "${POSTGRES_PASSWORD}" = "**None**" ]; then
  echo "You need to set the POSTGRES_PASSWORD environment variable or link to a container named POSTGRES."
  exit 1
fi

if [ "${S3_ENDPOINT}" == "**None**" ]; then
  AWS_ARGS=""
else
  AWS_ARGS="--endpoint-url ${S3_ENDPOINT}"
fi

# env vars needed for aws tools
export AWS_ACCESS_KEY_ID=${S3_ACCESS_KEY_ID}
export AWS_SECRET_ACCESS_KEY=${S3_SECRET_ACCESS_KEY}
export AWS_DEFAULT_REGION=${S3_REGION}

export PGPASSWORD=$POSTGRES_PASSWORD
POSTGRES_HOST_OPTS="-h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER $POSTGRES_EXTRA_OPTS"

echo "Creating dump of ${POSTGRES_DATABASE} database from ${POSTGRES_HOST}..."
pg_dump $POSTGRES_HOST_OPTS $POSTGRES_DATABASE > dump.sql

echo "Compressing data..."
if [ "${DATA_FOLDERS_TO_BACKUP}" = "**None**" ]; then
  tar cvzf backup.tgz dump.sql
else
  tar cvzf backup.tgz dump.sql ${DATA_FOLDERS_TO_BACKUP}
fi

if [ "${METHOD}" = "S3" ]; then
  echo "Uploading achive to $S3_BUCKET"
  cat backup.tgz | aws $AWS_ARGS s3 cp - s3://$S3_BUCKET/$S3_PREFIX/${POSTGRES_DATABASE}_$(date +"%Y-%m-%dT%H:%M:%SZ").tgz || exit 2
else
  echo "Copy achive to ./backup/"
  cp backup.tgz ./backup/${POSTGRES_DATABASE}_$(date +"%Y-%m-%dT%H:%M:%SZ").tgz
  echo "Remove oldest backups"
  ls -tp ./backup/*.tgz | grep -v '/$' | tail -n +${DAYS_HISTORY}
  ls -tp ./backup/*.tgz | grep -v '/$' | tail -n +${DAYS_HISTORY} | xargs -I {} rm -- {}
fi

echo "DB backuped successfully"

exit 0
