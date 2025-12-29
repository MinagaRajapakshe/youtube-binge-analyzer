from project import get_service, get_playlist_title, extract_playlist_id
import pytest

def test_extract_playlist_id():
    assert extract_playlist_id("https://www.youtube.com/playlist?list=PLhQjrBD2T383q7Vn8QnTsVgSvyLpsqL_R") == "PLhQjrBD2T383q7Vn8QnTsVgSvyLpsqL_R"
    
    with pytest.raises(ValueError, match="Invalid URL format."):
        extract_playlist_id("https://www.youtube.com/playlist?list=")