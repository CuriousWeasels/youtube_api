from googleapiclient.discovery import build
import json
import requests
import re
# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt
# from matplotlib.ticker import FuncFormatter

api_key = "xxx"

def get_channel_url():
    while True:
        channel_url = input("Paste link of youtube channel here: ")
        # Ensure that user paste the link as per copied from the youtube channel
        if re.search(r"^https://www.youtube.com/@", channel_url):
            return channel_url
        else:
            print("Invalid link. Please try again."
                  "Remember to copy directly from the channel profile.")
    

def get_channel_id(channel_url):
    # Retrieve channel IDs from page source
    pattern = re.compile(r'href="https://www.youtube.com/channel/([a-zA-Z0-9_-]+)"')
    respond = requests.get(channel_url)
    if respond.status_code == 200:
        match = pattern.search(respond.text)
        if match:
            return match.group(1)
        else:
            print(f"Invalid profile link for {channel_url}")
    else:
        print(
            f"Failed to retrieve the webpage:"
            f" {channel_url}\nStatus code: {respond.status_code}")

def get_channel_name(channel_id):
    youtube = build("youtube", "v3", developerKey=api_key)
    request = youtube.channels().list(
        part="snippet",
        id=channel_id
    )

    response = request.execute()
    channel_details = {}
    return response["items"][0]["snippet"]["title"]

def get_playlists(channel_id):
    playlists = []
    youtube = build("youtube", "v3", developerKey=api_key)
    request = youtube.playlists().list(
        part="contentDetails, snippet",
        channelId=channel_id,
        maxResults = 50
    )
    response = request.execute()

    for item in response["items"]:
        
        playlist_dict = {}
        playlist_dict["Playlist Title"] = item["snippet"]["title"]
        playlist_dict["Playlist ID"] = item["id"]
        playlist_dict["Video Count"] = item["contentDetails"]["itemCount"]
        playlists.append(playlist_dict)

    nextPageToken = response.get("nextPageToken")
    while nextPageToken:
        request = youtube.playlists().list(
            part="contentDetails, snippet",
            channelId=channel_id,
            maxResults = 50
            )

        for item in response["items"]:
            
            playlist_dict = {}
            playlist_dict["Playlist Title"] = item["snippet"]["title"]
            playlist_dict["Playlist ID"] = item["id"]
            playlist_dict["Video Count"] = item["contentDetails"]["itemCount"]
            playlists.append(playlist_dict)
        
        nextPageToken = response.get("nextPageToken")

    return playlists


def get_playlist_video(playlist_id):
    video_id = []
    youtube = build("youtube", "v3", developerKey=api_key)
    request = youtube.playlistItems().list(
        part="snippet, contentDetails",
        maxResults=50,
        playlistId=playlist_id
        )
    
    response = request.execute()
    
    for item in response["items"]:
        video_id.append(item["contentDetails"]["videoId"])

    nextPageToken = response.get("nextPageToken")
    while nextPageToken:
        request = youtube.playlistItems().list(
            part="snippet, contentDetails",
            maxResults=50,
            playlistId=playlist_id,
            pageToken = nextPageToken)
        response = request.execute()

        for item in response["items"]:
            print(item["contentDetails"]["videoId"])

        nextPageToken = response.get("nextPageToken")
        video_id.append(item["contentDetails"]["videoId"])

    return video_id

    # return [Video Title: xxx, Video ID: xxx]

def hastrue():
    return True

def hasfalse():
    return False

def main():
    # channel_url = get_channel_url()
    channel_id = get_channel_id("https://www.youtube.com/@freecodecamp")
    channel_title = get_channel_name(channel_id)
    channel_playlists_dict = get_playlists(channel_id)
    # [{'Playlist Title': 'Livestreams | Alex Phillips',
    # 'Playlist ID': 'PLcEme9FYiqT9gYtGn3G04FUUMMLL-UXS4',
    # 'Video Count': 3}]
    for items in channel_playlists_dict:
        items["Videos"] = get_playlist_video(items["Playlist ID"])
    
    print(channel_playlists_dict)

    # Test PLWKjhJtqVAbnupwRFOq9zGOWjdvPRtCmO Playlist ID with more than 50 videos
if __name__ == "__main__":
    main()
