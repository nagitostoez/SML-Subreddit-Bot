# SML Subreddit Bot

This bot automatically posts new videos from a specified YouTube channel to a Reddit subreddit. It applies flair to the post, makes it sticky, and distinguishes it as a mod post for maximum visibility.

## Features
- Fetches the latest video from a specified YouTube channel.
- Posts the video as a link post to a Reddit subreddit.
- Applies flair to the post and makes it sticky and a mod post.
- Prevents duplicate posts by tracking the last posted video.
- Configurable via environment variables.

## Requirements
- Python 3.x
- `praw` - Python Reddit API Wrapper
- `requests` - HTTP library to make requests to the YouTube API
- `python-dotenv` - To load environment variables from a `.env` file

## Installation & Setup

### 1. Clone the repository
To clone the repository, run the following command:

```bash
git clone https://github.com/nagitostoez/SML-Subreddit-Bot
```

### 2. Install dependencies
Install the necessary dependencies using `pip`:

```bash
pip install -r requirements.txt
```

### 3. Create a `.env` file
Create a `.env` file in the root directory of the project with the following environment variables:

```ini
YOUTUBE_API_KEY=your_youtube_api_key
CHANNEL_ID=your_youtube_channel_id
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USERNAME=your_reddit_username
REDDIT_PASSWORD=your_reddit_password
SUBREDDIT_NAME=your_subreddit_name
```

### 4. Running the bot
Once the setup is complete, run the bot using the following command:

```bash
python bot.py
```

### 5. Customizing the Bot
- **Flair ID**: You can change the flair ID by modifying the `FLAIR_ID` in the script.
- **Post Content**: Customize the post content by editing the `post_to_reddit()` function in the bot.

## How It Works
1. The bot checks for new videos from the specified YouTube channel every 30 seconds.
2. When a new video is found, the bot automatically posts it to the specified Reddit subreddit with the assigned flair.
3. The bot ensures no duplicate posts are made by tracking the title of the last posted video.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing
Feel free to fork this repository, submit issues, or create pull requests for improvements!

## Disclaimer
Please use this bot responsibly to avoid violating Reddit’s terms of service or hitting YouTube API quota limits.
```
