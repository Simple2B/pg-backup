FROM python:3.11

ADD install.sh install.sh
RUN bash install.sh && rm install.sh

ENV POSTGRES_DATABASE **None**
ENV POSTGRES_HOST **None**
ENV POSTGRES_PORT 5432
ENV POSTGRES_USER **None**
ENV POSTGRES_PASSWORD **None**
ENV POSTGRES_EXTRA_OPTS ''

ENV S3_ACCESS_KEY_ID **None**
ENV S3_SECRET_ACCESS_KEY **None**
ENV S3_BUCKET **None**
ENV S3_REGION us-west-1
ENV S3_PATH 'backup'
ENV S3_ENDPOINT **None**
ENV S3_S3V4 no
ENV SCHEDULE **None**
ENV DROP_PUBLIC 'yes'
ENV DATA_FOLDERS_TO_BACKUP **None**
ENV DAYS_HISTORY 30
ENV PATH /.venv/bin:$PATH

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock
COPY poetry.toml poetry.toml
RUN poetry install --without dev
COPY ./tasks /tasks

ADD run.sh run.sh
ADD backup.sh backup.sh
ADD restore.sh restore.sh
RUN chmod +x run.sh backup.sh restore.sh


CMD ["sh", "run.sh"]
