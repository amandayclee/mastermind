import logging
from src.interface.game_interface import GameInterface
from src.utils.logging_config import setup_logging_config

logger = logging.getLogger(__name__)

def main():
    setup_logging_config()
    logger.info("Starting Mastermind game application")
    
    cli = GameInterface()
    logger.info("Game interface initialized successfully")
    
    cli.start_menu()
    logger.info("Game application terminated normally")

if __name__ == "__main__":
    main()