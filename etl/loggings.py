from logging import getLogger, StreamHandler
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='../django_api/.env')

level = os.environ.get('LOG_LEVEL')

logger = getLogger(__name__)
logger.addHandler(StreamHandler())
logger.setLevel(level=level)
