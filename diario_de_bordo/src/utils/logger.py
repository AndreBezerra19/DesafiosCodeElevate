from loguru import logger

def setup_logger():
    """Configura o logger."""
    logger.add("logs/diario_de_bordo.log", rotation="10 MB", retention="7 days", level="INFO")
    return logger