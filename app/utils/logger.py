from loguru import logger
logger.add("logs/app.log", rotation="10 MB")





from app.utils.logger import logger
logger.info("New user registered")