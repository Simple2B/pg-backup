from invoke import task
from .config import config
from .logger import log

CFG = config()


@task
def backup(ctx):
    """Backup database"""
    log(log.INFO, "Backup started")
    ctx.run("sh backup.sh")
    log(log.INFO, "Backup finished")
