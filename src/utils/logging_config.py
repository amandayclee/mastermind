import logging
from pathlib import Path


def setup_logging_config(log_directory: str = "app_logs") -> None:
    log_path = Path(log_directory) # where you call this function
    log_path.mkdir(exist_ok=True) 
    
    logger = logging.getLogger("src")
    logger.setLevel(logging.INFO)
    
    
    if logger.hasHandlers():
        logger.handlers.clear()
        
    file_handler = logging.FileHandler(log_path / "mastermind.log")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(
        logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    )
    
    logger.addHandler(file_handler)