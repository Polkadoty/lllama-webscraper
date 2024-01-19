import praw
import requests
import os
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

reddit = praw.Reddit(client_id=config['reddit']['client_id'],
                     client_secret=config['reddit']['client_secret'],
                     user_agent='your_user_agent',
                     username=config['reddit']['username'],
                     password=config['reddit']['password'])

subreddit = reddit.subreddit('LocalLlama')

for post in subreddit.hot(limit=10):  # Adjust the limit as needed
    # Code to handle each post
    # Example: Downloading images
    if post.url.endswith(('.jpg', '.png')):
        response = requests.get(post.url)
        if response.status_code == 200:
            with open(os.path.join('path_to_save', post.id + '.jpg'), 'wb') as f:
                f.write(response.content)