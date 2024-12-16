import logging
from logging import Logger
import datetime

logging.basicConfig(level=logging.INFO, filename=f"logs/{datetime.date.today()}.log",filemode="a", encoding='utf-8',
                    format="%(asctime)s %(levelname)s %(message)s")

logger = logging.getLogger(__name__)