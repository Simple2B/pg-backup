from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from invoke import Context, task

from .logger import log
from .config import config
from .backup import backup

CFG = config()


def backup_run():
    log(log.INFO, "Backup runner started")
    backup(Context())


@task
def scheduler(ctx: Context):
    """Scheduler"""
    log(log.INFO, "Scheduler started")
    log(log.DEBUG, "Scheduler config: %s", CFG)

    scheduler = BlockingScheduler()
    trigger = CronTrigger(
        hour=CFG.SCHEDULE_HOUR,
        minute=CFG.SCHEDULE_MINUTE,
        year=CFG.SCHEDULE_YEAR,
        month=CFG.SCHEDULE_MONTH,
        day=CFG.SCHEDULE_DAY,
        week=CFG.SCHEDULE_WEEK,
        day_of_week=CFG.SCHEDULE_DAY_OF_WEEK,
        second=CFG.SCHEDULE_SECOND,
    )
    log(log.DEBUG, "Scheduler trigger: %s", trigger)
    scheduler.add_job(
        backup_run,
        trigger=trigger,
    )
    scheduler.start()
