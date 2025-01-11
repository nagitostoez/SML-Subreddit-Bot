import praw
import requests
import time
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Environment variables
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
CHANNEL_ID = os.getenv("CHANNEL_ID")
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")
SUBREDDIT_NAME = os.getenv("SUBREDDIT_NAME")
LAST_POSTED_FILE = "last_posted_video.txt"  # File to store the last posted video

# Function to get the latest video from the specified YouTube channel
def get_latest_video(api_key, channel_id):
    url = f"https://www.googleapis.com/youtube/v3/search?key={api_key}&channelId={channel_id}&order=date&part=snippet"
    response = requests.get(url).json()

    # Check if there are any videos
    if response.get("items"):
        video = response["items"][0]  # Get the first video from the response
        video_title = video["snippet"]["title"]
        video_url = f"https://www.youtube.com/watch?v={video['id']['videoId']}"
        return video_title, video_url
    else:
        print("No videos found!")
        return None, None

# Function to post to Reddit
def post_to_reddit(video_title, video_url):
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent='python:sml_reddit_bot:v1.0 (by u/your_username)',
        username=REDDIT_USERNAME,
        password=REDDIT_PASSWORD,
    )

    subreddit = reddit.subreddit(SUBREDDIT_NAME)
    post_title = f"Discussion Thread: {video_title}"
    post_content = f"**Video URL:** {video_url}\n\nLet's discuss!"

    subreddit.submit(post_title, selftext=post_content, stickied=True)
    print(f"Posted discussion thread: {post_title}")

# Function to read the last posted video from the file
def read_last_posted_video():
    if os.path.exists(LAST_POSTED_FILE):
        with open(LAST_POSTED_FILE, "r") as file:
            return file.read().strip()
    return None

# Function to save the last posted video to the file
def save_last_posted_video(video_title):
    with open(LAST_POSTED_FILE, "w") as file:
        file.write(video_title)

# Main function to check for new video and post
def main():
    print("Bot is starting...")

    # Track previously posted video to avoid duplicates
    last_posted_video = read_last_posted_video()  # Load the last posted video from the file

    while True:
        print("Checking for new videos...")

        # Get the latest video
        video_title, video_url = get_latest_video(YOUTUBE_API_KEY, CHANNEL_ID)

        if video_title and video_url:
            # If the video is new and hasn't been posted already
            if video_title != last_posted_video:
                print(f"New video found: {video_title}. Posting to Reddit...")
                post_to_reddit(video_title, video_url)
                save_last_posted_video(video_title)  # Save the new video as the last posted video
                last_posted_video = video_title
            else:
                print("No new video found, skipping...")
        else:
            print("No video to post!")

        # Sleep for 10 minutes before checking again
        print("Waiting 10 minutes before next check...")
        time.sleep(600)  # 10 minutes

if __name__ == "__main__":
    main()
