# pg-backup

Backup Postgres db and data files to mounted volume /backup

## Usage

Docker Compose:

```yaml
db:
  image: postgres:14
  volumes:
    - db_data:/var/lib/postgresql/data
  environment:
    POSTGRES_USER: ${POSTGRES_USER:-postgres}
    POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-passwd}
    POSTGRES_DB: db
    PGDATABASE: db
    PGPASSWORD: ${POSTGRES_PASSWORD:-passwd}
    PGUSER: ${POSTGRES_USER:-postgres}
  ports:
    - 127.0.0.1:${LOCAL_DB_PORT:-15432}:5432

backup:
  image: simple2b/pg-backup:latest # set desired version
  links:
    - db
  volumes:
    - ./backup:/backup
  environment:
    # scheduler for every 3 days
    SCHEDULE_DAY: ${SCHEDULE_DAY:-3}
    POSTGRES_DATABASE: db
    POSTGRES_HOST: db
    POSTGRES_USER: ${POSTGRES_USER:-postgres}
    POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-passwd}
    POSTGRES_EXTRA_OPTS: "--schema=public --blobs"
    DAYS_HISTORY: 7
    S3_REGION: ${S3_REGION:-**None**}
    S3_ACCESS_KEY_ID: ${S3_ACCESS_KEY_ID:-**None**}
    S3_SECRET_ACCESS_KEY: ${S3_SECRET_ACCESS_KEY:-**None**}
    S3_BUCKET: ${S3_BUCKET:-**None**}
    S3_PREFIX: ${S3_PREFIX:-**None**}
    AWS_ACCESS_KEY_ID: ${S3_ACCESS_KEY_ID:-**None**}
    AWS_SECRET_ACCESS_KEY: ${S3_SECRET_ACCESS_KEY:-**None**}
    AWS_DEFAULT_REGION: ${S3_REGION:-**None**}
```

### Automatic Periodic Backups

`DAYS_HISTORY` - variable defines period in days, after that backup files will be removed
`SCHEDULE_HOUR` - crontab variable that defines hours
`SCHEDULE_MINUTE` - crontab variable that defines minutes
`SCHEDULE_SECOND:` - crontab variable that seconds
`SCHEDULE_YEAR` - crontab variable that defines year
`SCHEDULE_MONTH` - crontab variable that defines month
`SCHEDULE_DAY` - crontab variable that defines day of month
`SCHEDULE_WEEK` - crontab variable that defines week of month
`SCHEDULE_DAY_OF_WEEK` - crontab variable that defines day of week
`SCHEDULE_START_DATE` - crontab variable that defines
`SCHEDULE_END_DATE` - crontab variable that defines

### Manually create backup

For manually run database backup you need goto project folder and execute the following line.

```bash
docker compose exec backup sh backup.sh
```

### Manually restore latest stored backup

For restore the latest backup you need goto project folder and execute the following line.

```bash
docker compose exec backup sh restore.sh
```

**Warning!**
This will potentially put your database in a very bad state or complete destroy your data, be very careful.# pg-backup
