import pytest
from unittest.mock import Mock, patch
from src.utils.validators import InputValidator, ValidationResult

class TestInputValidator:
    
    @pytest.fixture
    def mock_validator(self, game_config):
        return InputValidator(game_config)

    def test_validate_guess_input_valid(self, mock_validator):
        """
        Test validation of valid guess inputs
        """
        valid_inputs = [
            "1234",
            "1 2 3 4",
            "0000",
            "7070"
        ]
        
        for input_str in valid_inputs:
            result = mock_validator.validate_guess_input(input_str)
            assert isinstance(result, ValidationResult)
            assert result.is_valid is True
            assert result.message == ""
            assert result.error_code == ""

    def test_validate_guess_input_empty(self, mock_validator):
        """
        Test validation of empty guess input
        """
        result = mock_validator.validate_guess_input("")
        assert isinstance(result, ValidationResult)
        assert result.is_valid is False
        assert result.message == "Input cannot be empty"
        assert result.error_code == "EMPTY_INPUT"

        # Test whitespace only
        result = mock_validator.validate_guess_input("   ")
        assert result.is_valid is False
        assert result.message == "Input cannot be empty"
        assert result.error_code == "EMPTY_INPUT"

    def test_validate_guess_input_non_numeric(self, mock_validator):
        """
        Test validation of non-numeric guess inputs
        """
        invalid_inputs = [
            "123a",     # Contains letter
            "12.34",    # Contains decimal
            "12#34",    # Contains special character
            "abcd"      # All letters
        ]
        
        for input_str in invalid_inputs:
            result = mock_validator.validate_guess_input(input_str)
            assert result.is_valid is False
            assert result.message == "Input must contain only numbers"
            assert result.error_code == "NON_NUMERIC"

    def test_validate_guess_input_wrong_length(self, mock_validator):
        """
        Test validation of guess inputs with wrong length
        """
        invalid_inputs = [
            "123",          # Too short
            "12345",        # Too long
            "1 2 3",        # Too few numbers
            "1 2 3 4 5"     # Too many numbers
        ]
        
        expected_msg = f"Must enter exactly {mock_validator.config.pattern_length} numbers"
        
        for input_str in invalid_inputs:
            result = mock_validator.validate_guess_input(input_str)
            assert result.is_valid is False
            assert result.message == expected_msg
            assert result.error_code == "INVALID_LENGTH"

    def test_parse_guess_input_without_spaces(self, mock_validator):
        """
        Test parsing of guess input without spaces
        """
        input_str = "1234"
        result = mock_validator.parse_guess_input(input_str)
        assert result == [1, 2, 3, 4]

    def test_parse_guess_input_with_spaces(self, mock_validator):
        """
        Test parsing of guess input with spaces
        """
        input_str = "1 2 3 4"
        result = mock_validator.parse_guess_input(input_str)
        assert result == [1, 2, 3, 4]

    def test_validate_number_range_valid(self, mock_validator):
        """
        Test validation of numbers within valid range
        """
        valid_numbers = [
            [0, 1, 2, 3],
            [7, 7, 7, 7],
            [0, 0, 0, 0],
            [4, 5, 6, 7]
        ]
        
        for numbers in valid_numbers:
            result = mock_validator.validate_number_range(numbers)
            assert result.is_valid is True
            assert result.message == ""
            assert result.error_code == ""

    def test_validate_number_range_invalid(self, mock_validator):
        """
        Test validation of numbers outside valid range
        """
        invalid_numbers = [
            [-1, 1, 2, 3],    # Below min
            [1, 8, 2, 3],     # Above max
            [8, 8, 8, 8],     # All above max
            [-1, -1, -1, -1]  # All below min
        ]
        
        expected_msg = f"Numbers must be between {mock_validator.config.min_number} and {mock_validator.config.max_number}"
        
        for numbers in invalid_numbers:
            result = mock_validator.validate_number_range(numbers)
            assert result.is_valid is False
            assert result.message == expected_msg
            assert result.error_code == "OUT_OF_RANGE"

    def test_validate_game_id_valid(self, mock_validator):
        """
        Test validation of valid game ID
        """
        valid_id = "123e4567-e89b-12d3-a456-426614174000"
        result = mock_validator.validate_game_id(valid_id)
        assert result.is_valid is True
        assert result.message == ""
        assert result.error_code == ""

    def test_validate_game_id_empty(self, mock_validator):
        """
        Test validation of empty game ID
        """
        result = mock_validator.validate_game_id("")
        assert result.is_valid is False
        assert result.message == "Game ID cannot be empty"
        assert result.error_code == "EMPTY_ID"

    def test_validate_game_id_whitespace(self, mock_validator):
        """
        Test validation of whitespace game ID
        """
        result = mock_validator.validate_game_id("   ")
        assert result.is_valid is False
        assert result.message == "Game ID cannot be only whitespace"
        assert result.error_code == "WHITESPACE_ID"

    def test_validate_game_id_invalid_format(self, mock_validator):
        """
        Test validation of invalid game ID format
        """
        invalid_ids = [
            "not-a-uuid",
            "123",
            "123e4567-e89b-12d3-a456-42661417400!"
        ]
        
        for game_id in invalid_ids:
            result = mock_validator.validate_game_id(game_id)
            assert result.is_valid is False
            assert result.message == "Invalid game ID format"
            assert result.error_code == "INVALID_ID_FORMAT"

    def test_validate_difficulty_selection_valid(self, mock_validator):
        """
        Test validation of valid difficulty selections
        """
        valid_selections = ["1", "2"]
        
        for selection in valid_selections:
            result = mock_validator.validate_difficulty_selection(selection)
            assert result.is_valid is True
            assert result.message == ""
            assert result.error_code == ""

    def test_validate_difficulty_selection_empty(self, mock_validator):
        """
        Test validation of empty difficulty selection
        """
        result = mock_validator.validate_difficulty_selection("")
        assert result.is_valid is False
        assert result.message == "Please select a difficulty level"
        assert result.error_code == "EMPTY_SELECTION"

        result = mock_validator.validate_difficulty_selection("   ")
        assert result.is_valid is False
        assert result.message == "Please select a difficulty level"
        assert result.error_code == "EMPTY_SELECTION"

    def test_validate_difficulty_selection_invalid(self, mock_validator):
        """
        Test validation of invalid difficulty selections
        """
        invalid_selections = ["0", "3", "a", "#"]
        
        for selection in invalid_selections:
            result = mock_validator.validate_difficulty_selection(selection)
            assert result.is_valid is False
            assert result.message == "Please select 1 for Normal or 2 for Hard"
            assert result.error_code == "INVALID_DIFFICULTY"

    def test_update_config(self, mock_validator):
        """
        Test updating validator configuration
        """
        new_config = Mock()
        new_config.pattern_length = 6
        new_config.min_number = 0
        new_config.max_number = 9
        
        mock_validator.update_config(new_config)
        assert mock_validator.config == new_config
        
        result = mock_validator.validate_guess_input("123456")
        assert result.is_valid is True
        
        result = mock_validator.validate_guess_input("1234")
        assert result.is_valid is False
        assert result.error_code == "INVALID_LENGTH"