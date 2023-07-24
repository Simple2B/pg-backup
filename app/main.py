from . import scheduler
from .logger import log
from .config import config

CFG = config()

if __name__ == "__main__":
    log.set_level(CFG.LOG_LEVEL)
    log(log.INFO, "App started in %s mode", CFG.ENV)
    scheduler()
