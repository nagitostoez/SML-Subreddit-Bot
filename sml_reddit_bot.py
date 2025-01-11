import os
import praw
import googleapiclient.discovery
import googleapiclient.errors
from dotenv import load_dotenv
import time

load_dotenv()  # Load environment variables from .env

# Get the environment variables
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
CHANNEL_ID = os.getenv("CHANNEL_ID")
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = "script:bot:v1.0 (by u/your_reddit_username)"  # Set your user agent
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")
SUBREDDIT_NAME = os.getenv("SUBREDDIT_NAME")

import html  # Add this import at the top

def get_latest_video(api_key, channel_id):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        order="date",
        maxResults=1
    )
    response = request.execute()

    # Debug print to check the API response
    print("YouTube API response:", response)

    if "items" not in response or len(response["items"]) == 0:
        print("No videos found!")
        return None, None

    video = response["items"][0]
    video_title = video["snippet"]["title"]
    video_title = html.unescape(video_title)  # Decode HTML entities like &#39; to apostrophe
    video_url = f"https://www.youtube.com/watch?v={video['id']['videoId']}"
    return video_title, video_url

def post_to_reddit(title, url):
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_SECRET,
        user_agent=REDDIT_USER_AGENT,
        username=REDDIT_USERNAME,
        password=REDDIT_PASSWORD
    )
    subreddit = reddit.subreddit(SUBREDDIT_NAME)
    post = subreddit.submit(title, url=url)
    post.mod.sticky()  # Pin the post
    print(f"Posted and pinned: {title}")

def main():
    video_title, video_url = get_latest_video(YOUTUBE_API_KEY, CHANNEL_ID)
    if video_title and video_url:
        post_to_reddit(video_title, video_url)

if __name__ == "__main__":
    while True:
        main()
        time.sleep(60 * 30)  # Check every 30 minutes