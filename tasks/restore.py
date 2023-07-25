from invoke import task

from .config import config
from .logger import log

CFG = config()


@task
def restore(ctx):
    """Restore database"""
    log(log.INFO, "Restore started")
    ctx.run("sh restore.sh")
    log(log.INFO, "Restore finished")
