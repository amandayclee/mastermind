import logging
from typing import Dict, List
from src.config.game_config import GameConfig
from src.utils.exceptions import GeneratorError
from .base import NumberGenerator
import requests


logger = logging.getLogger(__name__)

class RandomOrgGenerator(NumberGenerator):
    """
    Number generator implementation using Random.org's HTTP API.
    
    Attributes:
        BASE_URL (str): Base URL for Random.org's integer generator API
        MAX_RETRIES (int): Maximum number of API call attempts before failing
    """
    
    BASE_URL = "https://www.random.org/integers/"
    MAX_RETRIES = 5
        
    def _get_api_params(self, config: GameConfig) -> Dict[str, str]:
        """
        Create parameter dictionary for Random.org API call.
        
        Args:
            config: Game configuration containing number generation parameters

        Returns:
            Dictionary of parameters formatted for the Random.org API
        """
        return {
            "num": str(config.pattern_length),
            "min": str(config.min_number),
            "max": str(config.max_number),
            "col": str(config.pattern_length),
            "base": "10",
            "format": "plain",
            "rnd": "new"
        }
        
    def _build_url(self, api_params: Dict[str, setattr]) -> str:
        """
        Construct the full API URL with parameters.
        
        Args:
            api_params: Dictionary of API parameters

        Returns:
            Complete URL string for the API request
        """
        return self.BASE_URL + "?" + "&".join(f"{key}={value}" for key, value in api_params.items())
    
    def generate(self, config: GameConfig) -> List[int]:
        """
        Generate random numbers using Random.org's API.
        
        Implements retry logic for failed API calls and handles response parsing.
        
        Args:
            config: Game configuration containing number generation parameters

        Returns:
            List of randomly generated integers

        Raises:
            GeneratorError: If all retry attempts fail
        """
        retries = 0
        while retries < self.MAX_RETRIES:
            try:
                api_params = self._get_api_params(config)
                api_link = self._build_url(api_params)
                
                response = requests.get(api_link)
                response.raise_for_status()
                code_pattern = [int(_) for _ in response.text.strip("\n").split("\t")]
                logger.info("Successfully generated numbers from Random.org")
                
                return code_pattern
            
            except requests.exceptions.RequestException as e:
                retries += 1
                logger.warning(f"API call attempt {retries} failed: {e}")

                if retries == self.MAX_RETRIES:
                    raise GeneratorError(f"Failed to generate numbers after {self.MAX_RETRIES} attempts: {e}")