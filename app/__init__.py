from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
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
        scheduler.add_job(
            backup,
            CronTrigger(
                hour=CFG.SCHEDULE_HOUR,
                minute=CFG.SCHEDULE_MINUTE,
                year=CFG.SCHEDULE_YEAR,
                month=CFG.SCHEDULE_MONTH,
                day=CFG.SCHEDULE_DAY,
                week=CFG.SCHEDULE_WEEK,
                day_of_week=CFG.SCHEDULE_DAY_OF_WEEK,
                second=CFG.SCHEDULE_SECOND,
                start_date=CFG.SCHEDULE_START_DATE,
                end_date=CFG.SCHEDULE_END_DATE,
            ),
        )
        scheduler.start()
