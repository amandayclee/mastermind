from .base import NumberGenerator
import requests

class RandomOrgGenerator(NumberGenerator):
    def generate(self, config):
        while True:
            try:
                api_params = config.get_api_params()
                api_link = config.api_base_url + "?" + "&".join(f"{key}={value}" for key, value in api_params.items())
                
                response = requests.get(api_link)
                response.raise_for_status()
                code_pattern = [int(_) for _ in response.text.strip("\n").split("\t")]
                return code_pattern
            
            except requests.exceptions.RequestException as e:
                print(f"{e}, API request failed.")