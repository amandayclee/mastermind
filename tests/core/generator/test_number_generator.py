import pytest
import requests
from unittest.mock import patch, Mock
from src.core.generators.random_org import RandomOrgGenerator
from src.utils.exceptions import GeneratorError

class TestRandomGenerator:
    @pytest.fixture
    def generator(self):
        return RandomOrgGenerator()
    
    def test_get_api_params(self, generator, game_config):
        """Test API parameters generation"""
        params = generator._get_api_params(game_config)
        
        assert params == {
            "num": "4",
            "min": "0",
            "max": "7",
            "col": "4",
            "base": "10",
            "format": "plain",
            "rnd": "new"
        }
        
    def test_build_url(self, generator, game_config):
        """Test URL building with parameters"""
        params = generator._get_api_params(game_config)
        url = generator._build_url(params)
        
        assert url.startswith(generator.BASE_URL)
        assert "num=4" in url
        assert "min=0" in url
        assert "max=7" in url
        
    @patch('requests.get')
    def test_successful_generation(self, mock_get, generator, game_config):
        """Test successful number generation"""
        mock = Mock()
        mock.text = "1\t2\t3\t4"
        mock.raise_for_status.return_value = None
        mock_get.return_value = mock
        
        pattern = generator.generate(game_config)
        assert pattern == [1, 2, 3, 4]

    @patch('requests.get')
    def test_connection_error_generation(self, mock_get, generator, game_config):
        """Test handling of HTTP errors"""
        mock_get.side_effect = requests.exceptions.ConnectionError("Network is unreachable")
        
        with pytest.raises(GeneratorError) as excinfo:
            generator.generate(game_config)
            
        assert "Failed to generate numbers" in str(excinfo.value)
        assert mock_get.call_count == generator.MAX_RETRIES
        
    @patch('requests.get')
    def test_http_error_generation(self, mock_get, generator, game_config):
        """Test handling of HTTP errors"""
        mock = Mock()
        mock.status_code = 503
        mock.raise_for_status.side_effect = requests.exceptions.HTTPError("503 Server Error")
        mock_get.return_value = mock
        
        with pytest.raises(GeneratorError) as excinfo:
            generator.generate(game_config)
            
        assert "Failed to generate numbers" in str(excinfo.value)
        assert mock_get.call_count == generator.MAX_RETRIES
    
    @patch('requests.get')
    def test_retry_success(self, mock_get, generator, game_config):
        """Test retry after failures"""
        mock_error = Mock()
        mock_error.raise_for_status.side_effect = requests.exceptions.HTTPError("503 Server Error")
        
        mock_success = Mock()
        mock_success.text = "1\t2\t3\t4\n"
        mock_success.raise_for_status.return_value = None
        
        mock_get.side_effect = [mock_error, mock_error, mock_success]
        
        pattern = generator.generate(game_config)
        
        assert pattern == [1, 2, 3, 4]
        assert mock_get.call_count == 3