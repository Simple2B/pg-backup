from apscheduler.schedulers.background import BackgroundScheduler

from .logger import log
from .config import config

CFG = config()


def backup():
    log(log.INFO, "Backup started")


def restore():
    log(log.INFO, "Restore started")


def scheduler():
    log(log.INFO, "Scheduler started")
    with BackgroundScheduler() as scheduler:
        scheduler: BackgroundScheduler
        scheduler.add_job(backup, "cron", hour=0, minute=0)
        scheduler.start()
