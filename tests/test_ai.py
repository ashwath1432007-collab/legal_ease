import pytest
from unittest.mock import patch, MagicMock
from ai_core.gemini_generator import GeminiGenerator


def test_generator_init_missing_api_key():
    with patch.dict('os.environ', {}, clear=True):
        with pytest.raises(ValueError):
            GeminiGenerator()


@pytest.mark.asyncio
async def test_generate_success():
    with patch.dict('os.environ', {'GEMINI_API_KEY': 'test_key'}):
        generator = GeminiGenerator()
        mock_response = MagicMock()
        mock_response.text = "Test document content"
        generator.model = MagicMock()
        generator.model.generate_content.return_value = mock_response

        result = await generator.generate("NDA", "Test parties", "Test terms", "2026-09-30")
        assert "Test document content" in result
        assert "DISCLAIMER" in result


@pytest.mark.asyncio
async def test_generate_api_error():
    with patch.dict('os.environ', {'GEMINI_API_KEY': 'test_key'}):
        generator = GeminiGenerator()
        generator.model = MagicMock()
        generator.model.generate_content.side_effect = Exception("API Error")

        with pytest.raises(ValueError):
            await generator.generate("NDA", "Test", "Test", "2026-09-30")
