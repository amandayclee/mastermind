import pytest
import requests
from unittest.mock import patch, Mock
from src.core.config.game_config import GameConfig
from src.core.models.game_difficulty import Difficulty
from src.services.generators.random_org import RandomOrgGenerator
from src.services.exceptions.exceptions import GeneratorError

class TestRandomGenerator:
    @pytest.fixture
    def generator(self):
        return RandomOrgGenerator()
    
    @pytest.fixture(params=[Difficulty.NORMAL, Difficulty.HARD])
    def game_config(self, request):
        """
        Creates different game configs for testing
        """
        return GameConfig(difficulty=request.param)
    
    def test_get_api_params(self, generator, game_config):
        """
        Test API parameters generation for different configurations
        """
        params = generator._get_api_params(game_config)
        
        expected_length = "4" if game_config.difficulty == Difficulty.NORMAL else "5"
        expected_max = "7" if game_config.difficulty == Difficulty.NORMAL else "9"
        
        assert params == {
            "num": expected_length,
            "min": "0",
            "max": expected_max,
            "col": expected_length,
            "base": "10",
            "format": "plain",
            "rnd": "new"
        }
        
    def test_build_url(self, generator, game_config):
        """
        Test URL building with parameters
        """
        params = generator._get_api_params(game_config)
        url = generator._build_url(params)
        
        expected_length = "4" if game_config.difficulty == Difficulty.NORMAL else "5"
        expected_max = "7" if game_config.difficulty == Difficulty.NORMAL else "9"
        
        assert url.startswith(generator.BASE_URL)
        assert f"num={expected_length}" in url
        assert "min=0" in url
        assert f"max={expected_max}" in url
        
    @patch('requests.get')
    def test_successful_generation(self, mock_get, generator, game_config):
        """
        Test successful number generation
        """
        expected_numbers = [1, 2, 3, 4] if game_config.difficulty == Difficulty.NORMAL else [1, 2, 3, 4, 5]
        mock = Mock()
        mock.text = "\t".join(map(str, expected_numbers))
        mock.raise_for_status.return_value = None
        mock_get.return_value = mock
        
        pattern = generator.generate(game_config)
        assert pattern == expected_numbers

    @patch('requests.get')
    def test_connection_error_generation(self, mock_get, generator, game_config):
        """
        Test handling of connection errors with fallback
        """
        mock_get.side_effect = requests.exceptions.ConnectionError("Network is unreachable")
        
        pattern = generator.generate(game_config)
            
        assert mock_get.call_count == generator.MAX_RETRIES
        assert len(pattern) == game_config.pattern_length
        assert all(game_config.min_number <= n <= game_config.max_number for n in pattern)
        
    @patch('requests.get')
    def test_http_error_with_fallback(self, mock_get, generator, game_config):
        """
        Test handling of HTTP errors with fallback
        """
        mock = Mock()
        mock.status_code = 503
        mock.raise_for_status.side_effect = requests.exceptions.HTTPError("503 Server Error")
        mock_get.return_value = mock
        
        pattern = generator.generate(game_config)
        
        assert mock_get.call_count == generator.MAX_RETRIES
        assert len(pattern) == game_config.pattern_length
        assert all(game_config.min_number <= n <= game_config.max_number for n in pattern)
        
    @patch('requests.get')
    def test_retry_success(self, mock_get, generator, game_config):
        """
        Test retry after failures
        """
        mock_error = Mock()
        mock_error.raise_for_status.side_effect = requests.exceptions.HTTPError("503 Server Error")
        
        expected_numbers = [1, 2, 3, 4] if game_config.difficulty == Difficulty.NORMAL else [1, 2, 3, 4, 5]
        mock_success = Mock()
        mock_success.text = "\t".join(map(str, expected_numbers))
        mock_success.raise_for_status.return_value = None
        
        mock_get.side_effect = [mock_error, mock_error, mock_success]
        
        pattern = generator.generate(game_config)
        
        assert pattern == expected_numbers
        assert mock_get.call_count == 3
        
    @patch('random.randint')
    def test_generate_fallback(self, mock_randint, generator, game_config):
        """
        Test fallback number generation
        """
        expected_numbers = list(range(game_config.pattern_length))
        mock_randint.side_effect = expected_numbers
        
        pattern = generator._generate_fallback(game_config)
        
        assert pattern == expected_numbers
        assert mock_randint.call_count == game_config.pattern_length
        
    @patch('requests.get')
    @patch('random.randint')
    def test_fallback_failure(self, mock_randint, mock_get, generator, game_config):
        """
        Test when both API and fallback generation fail
        """
        mock_get.side_effect = requests.exceptions.ConnectionError("Network is unreachable")
        mock_randint.side_effect = Exception("Random generation failed")
        
        with pytest.raises(GeneratorError) as exc_info:
            generator.generate(game_config)
        
        error_msg = str(exc_info.value)
        assert "Both API and fallback generation failed" in error_msg
        assert "Network is unreachable" in error_msg
        assert "Random generation failed" in error_msg