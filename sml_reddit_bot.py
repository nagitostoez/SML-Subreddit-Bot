import os
import praw
import googleapiclient.discovery
import googleapiclient.errors
from dotenv import load_dotenv
import time

# Load environment variables from .env file
load_dotenv()

# Get environment variables
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
CHANNEL_ID = os.getenv("CHANNEL_ID")
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")
SUBREDDIT_NAME = os.getenv("SUBREDDIT_NAME")

# Set up YouTube API client
def get_latest_video(api_key, channel_id):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        order="date",
        maxResults=1
    )
    response = request.execute()

    video = response["items"][0]
    video_title = video["snippet"]["title"]
    video_url = f"https://www.youtube.com/watch?v={video['id']['videoId']}"
    return video_title, video_url

# Set up Reddit API client
def create_reddit_post(title, url):
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        password=REDDIT_PASSWORD,
        username=REDDIT_USERNAME,
        user_agent="sml_reddit_bot"
    )

    # Create a new pinned post in the subreddit
    subreddit = reddit.subreddit(SUBREDDIT_NAME)
    post = subreddit.submit(title, url=url)
    post.mod.distinguish(sticky=True)  # Make the post pinned
    print(f"Successfully created a pinned post: {title}")

# Main function to check for new video and create Reddit post
def main():
    last_video_url = None
    while True:
        video_title, video_url = get_latest_video(YOUTUBE_API_KEY, CHANNEL_ID)
        if video_url != last_video_url:
            last_video_url = video_url
            create_reddit_post(video_title, video_url)
        else:
            print("No new video uploaded yet.")
        time.sleep(600)  # Check every 10 minutes

def store_last_video_id(video_id):
    with open('last_video_id.txt', 'w') as f:
        f.write(video_id)

def get_last_video_id():
    try:
        with open('last_video_id.txt', 'r') as f:
            return f.read()
    except FileNotFoundError:
        return None

def main():
    last_video_id = get_last_video_id()

    # Fetch the latest video details
    video_title, video_url = get_latest_video(YOUTUBE_API_KEY, CHANNEL_ID)
    
    # If a new video is found and it's not the same as the last posted one
    if video_title and video_url:
        video_id = video_url.split('v=')[-1]  # Extract the video ID from the URL
        
        # If this video is not the last one posted
        if video_id != last_video_id:
            post_to_reddit(video_title, video_url)
            store_last_video_id(video_id)  # Store this video ID as posted
        else:
            print("This video has already been posted.")
    else:
        print("No new video found!")

# Helper functions to store and get the last video ID
def store_last_video_id(video_id):
    with open('last_video_id.txt', 'w') as f:
        f.write(video_id)

def get_last_video_id():
    try:
        with open('last_video_id.txt', 'r') as f:
            return f.read()
    except FileNotFoundError:
        return None  # If the file doesn't exist, return None

if __name__ == "__main__":
    main()  # This will execute the main function when the script is run directly
