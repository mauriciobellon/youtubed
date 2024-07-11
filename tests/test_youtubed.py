import pytest
from click.testing import CliRunner
from youtubed.main import youtubed, get_processor, ensure_output_directory
from youtubed.utils.process_video import process_video
from youtubed.utils.process_playlist import process_playlist

def test_ensure_output_directory(tmp_path):
    test_dir = tmp_path / "test_output"
    ensure_output_directory(str(test_dir))
    assert test_dir.is_dir()

def test_get_processor_video():
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    assert get_processor(url) == process_video

def test_get_processor_playlist():
    url = "https://www.youtube.com/playlist?list=PLSomeListID"
    assert get_processor(url) == process_playlist

def test_get_processor_invalid():
    url = "https://www.youtube.com/invalid"
    with pytest.raises(ValueError):
        get_processor(url)

def test_youtubed_cli():
    runner = CliRunner()
    result = runner.invoke(youtubed, ["https://www.youtube.com/watch?v=dQw4w9WgXcQ"])
    assert result.exit_code == 0

def test_youtubed_cli_invalid_url():
    runner = CliRunner()
    result = runner.invoke(youtubed, ["https://www.youtube.com/invalid"])
    assert result.exit_code == 1
    assert "Invalid URL" in result.output