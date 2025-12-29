import os
import sys
from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import requests
import re

load_dotenv()

def main():
    # Get API service
    try:
        youtube = get_service()
        print("API Connection Successful")
    except ValueError as e:
        sys.exit(f"API Connection Failed: {e}")

    while True:
        playlist_confirmed = False

        url = input("Enter YouTube Playlist URL (or 'q' to quit): ").strip()
        
        if url.lower() in ['q', 'quit']:
            print("Exiting...")
            break
        
        try:
            playlist_id = extract_playlist_id(url)
        except Exception as e:
            print(f"\nError: {e} Please check the URL again.\n")
            continue

        try:
            # Pass the extracted ID to the function
            title = get_playlist_title(youtube, playlist_id) 
        except Exception as e:
            print(f"\nError: {e} Please check the URL and your connection\n")
        else:
            print(f"\nTarget Playlist: {title}\n")

            confirm = input("Is this the correct playlist? (y/n): ").lower().strip()
            while True:
                if confirm == 'y':
                    playlist_confirmed = True
                    break
                elif confirm == 'n':
                    playlist_confirmed = False
                    break
                else:
                    continue

        if playlist_confirmed:
            break

        # Proceed to calculation logic


def get_service():
    """
    Initializes the YouTube API discovery service.

    :return: The YouTube API service object.
    :raises ValueError: If the 'YOUTUBE_API_KEY' environment variable is missing.
    """
    api_key = os.getenv("YT_API_KEY")

    if not api_key:
        raise ValueError("YT_API_KEY not found in .env file.")
    
    return build("youtube", "v3", developerKey=api_key)


def get_playlist_title(youtube, playlist_id):
    """
    Retrieves the title of a YouTube playlist given its ID.

    :param youtube: The initialized YouTube API service object.
    :param playlist_id: The ID of the YouTube playlist.
    :return: The title of the playlist, or None if not found.
    """
    request = youtube.playlists().list(
        part="snippet",
        id=playlist_id
    )
    response = request.execute()

    if not response["items"]:
        raise ValueError("Playlist not found.")
        
    return response["items"][0]["snippet"]["title"]


def extract_playlist_id(url):
    """
    Extracts the YouTube playlist ID from a provided URL.

    :param url: The full YouTube playlist URL.
    :return: The extracted playlist ID string.
    :raises ValueError: If the URL format is invalid or no ID is found.
    """
    
    pattern = r"(?:list=)([a-zA-Z0-9_-]{18,42})"
    
    match = re.search(pattern, url)
    if match:
        playlist_id = match.group(1)
        return playlist_id
    else:
        raise ValueError("Invalid URL format.")

if __name__ == "__main__":
    main()