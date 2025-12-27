import os
import sys
from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import requests

load_dotenv()

def main():
    # Get API service
    try:
        youtube = get_service()
        print("API Connection Successful")
    except ValueError as e:
        sys.exit(f"API Connection Failed: {e}")

    while True:
        url = input("Enter YouTube Playlist URL (or 'q' to quit): ").strip()
        
        if url.lower() in ['q', 'quit']:
            print("Exiting...")
            break

        # playlist_id = extract_playlist_id(url) with regex
        playlist_id = url # temp
        # if not playlist_id:
        #     print("Invalid URL format. Please try again.")
        #     continue  

        try:
            # Pass the extracted ID to the function
            title = get_playlist_title(youtube, playlist_id) 
            print(f"\nTarget Playlist: {title}\n")
            
            confirm = input("Is this the correct playlist? (y/n): ").lower().strip()
            if confirm == 'y':
                # Proceed to calculation logic
                # total_seconds = get_playlist_duration(youtube, url)
                # display_results(total_seconds)
                break
                
        except Exception as e:
            print(f"Error: {e}. Please check the URL and your connection.\n")


def get_service():
    """
    Initializes the YouTube API discovery service.
    
    Returns: 
        The build object.
    Raises: 
        ValueError if API Key is missing.
    """
    api_key = os.getenv("YT_API_KEY")

    if not api_key:
        raise ValueError("YT_API_KEY not found in .env file.")
    
    return build("youtube", "v3", developerKey=api_key)


def get_playlist_title(youtube, playlist_id):
    """
    Retrieves the title of a YouTube playlist given its ID.

    Args:
        api_key (str): Your YouTube Data API v3 key.
        playlist_id (str): The ID of the YouTube playlist.

    Returns:
        str: The title of the playlist, or None if not found or an error occurs.
    """
    request = youtube.playlists().list(
        part="snippet",
        id=playlist_id
    )
    response = request.execute()

    if not response["items"]:
        raise ValueError("Playlist not found.")
        
    return response["items"][0]["snippet"]["title"]


if __name__ == "__main__":
    main()