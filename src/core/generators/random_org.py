from src.utils.exceptions import GeneratorError
from .base import NumberGenerator
import requests

class RandomOrgGenerator(NumberGenerator):
    BASE_URL = "https://www.random.org/integers/"
    MAX_RETRIES = 5
        
    def _get_api_params(self, config):
        return {
            "num": str(config.pattern_length),
            "min": str(config.min_number),
            "max": str(config.max_number),
            "col": str(config.pattern_length),
            "base": "10",
            "format": "plain",
            "rnd": "new"
        }
        
    def _build_url(self, api_params):
        return self.BASE_URL + "?" + "&".join(f"{key}={value}" for key, value in api_params.items())
    
    def generate(self, config):
        retries = 0
        while retries < self.MAX_RETRIES:
            try:
                api_params = self._get_api_params(config)
                api_link = self._build_url(api_params)
                
                response = requests.get(api_link)
                response.raise_for_status()
                code_pattern = [int(_) for _ in response.text.strip("\n").split("\t")]
                return code_pattern
            
            except requests.exceptions.RequestException as e:
                retries += 1
                print(f"Attempt {retries} failed: {e}")
                if retries == self.MAX_RETRIES:
                    raise GeneratorError(f"Failed to generate numbers after {self.MAX_RETRIES} attempts: {e}")