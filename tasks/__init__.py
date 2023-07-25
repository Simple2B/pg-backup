# flake8: noqa F401
import os
from .backup import backup
from .restore import restore
from .scheduler import scheduler
from .config import config
from .logger import log

CFG = config()
log.set_level(CFG.LOG_LEVEL)

for key, value in CFG.model_dump().items():
    os.environ[key] = str(value)
