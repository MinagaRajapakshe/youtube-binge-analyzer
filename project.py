import os
import sys
from dotenv import load_dotenv
from googleapiclient.discovery import build
import re
import isodate
from datetime import timedelta

def main():
    # Get API service
    try:
        youtube = get_service()
        # print("API Connection Successful") 
    except ValueError as e:
        sys.exit(f"API Connection Failed: {e}")

    playlist_id = None
    title = None

    while True:
        url = input("Enter YouTube Playlist URL (or 'q' to quit): ").strip()
        
        if url.lower() in ['q', 'quit']:
            sys.exit("Exiting...")
        
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
            continue
        
        print(f"\nTarget Playlist: {title}\n")

        confirm = input("Is this the correct playlist? (y/n): ").lower().strip()
        if confirm == 'y':
            break
        else:
            print("Please try again.")
            continue

    # Proceed to calculation logic
    if playlist_id:
        print(f"\nCalculating duration for: {title}...")
        get_playlist_duration(youtube, playlist_id)


def get_service():
    """
    Initializes the YouTube API discovery service.
    """
    load_dotenv()
    api_key = os.environ.get("YT_API_KEY")

    if not api_key:
        raise ValueError("YT_API_KEY environment variable not set.")
    
    return build("youtube", "v3", developerKey=api_key)


def get_playlist_title(youtube, playlist_id):
    """
    Retrieves the title of a YouTube playlist given its ID.
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
    """
    # Regex to handle various URL formats, including those with other query params
    pattern = r"(?:list=)([a-zA-Z0-9_-]+)"
    
    match = re.search(pattern, url)
    if match:
        playlist_id = match.group(1)
        return playlist_id
    else:
        raise ValueError("Invalid URL format.")


def get_playlist_duration(youtube, playlist_id):
    """
    Calculates and prints the total duration of the playlist at different speeds.
    """
    video_ids = []
    next_page_token = None

    # 1. Fetch all video IDs from the playlist
    while True:
        request = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response['items']:
            video_ids.append(item['contentDetails']['videoId'])

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    print(f"Found {len(video_ids)} videos. Fetching details...")

    # 2. Fetch video details (duration) in batches of 50
    total_seconds = 0
    
    for i in range(0, len(video_ids), 50):
        batch_ids = video_ids[i:i+50]
        request = youtube.videos().list(
            part="contentDetails",
            id=','.join(batch_ids)
        )
        response = request.execute()

        for item in response['items']:
            duration_iso = item['contentDetails']['duration']
            # isodate.parse_duration returns a datetime.timedelta object
            duration_td = isodate.parse_duration(duration_iso)
            total_seconds += duration_td.total_seconds()

    # 3. Calculate and Print
    print_time_stats(total_seconds)
    

def print_time_stats(total_seconds):
    """Helper to print duration at different speeds."""
    
    speeds = [1.0, 1.25, 1.5, 2.0]
    
    print("-" * 40)
    print(f"{'Speed':<10} | {'Time (HH:MM:SS)'}")
    print("-" * 40)

    for speed in speeds:
        adjusted_seconds = total_seconds / speed
        time_str = str(timedelta(seconds=int(adjusted_seconds)))
        print(f"{speed:<10} | {time_str}")
    print("-" * 40)

if __name__ == "__main__":
    main()