import praw
import requests
import json
import os
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

reddit = praw.Reddit(client_id=config['reddit']['client_id'],
                     client_secret=config['reddit']['client_secret'],
                     user_agent='windows:myllamabot:v1.0 (by /u/YourRedditUsername)',
                     username=config['reddit']['username'],
                     password=config['reddit']['password'])

subreddit = reddit.subreddit('LocalLlama')

output_dir = 'C:\\Programs\\LocalLlamaOutput'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for post in subreddit.hot(limit=10):  # Adjust the limit as needed
    post_data = {
        "title": post.title,
        "url": post.url,
        "body": post.selftext,
        "comments": []
    }

    # Expanding the comments
    post.comments.replace_more(limit=None)  # limit=None to get all comments
    for comment in post.comments.list():
        post_data["comments"].append({
            "author": comment.author.name if comment.author else "Deleted",
            "body": comment.body
        })

    # Saving post and comments to a file
    with open(os.path.join(output_dir, f'{post.id}.json'), 'w', encoding='utf-8') as f:
        json.dump(post_data, f, ensure_ascii=False, indent=4)

    # Downloading images if any
    if post.url.endswith(('.jpg', '.png')):
        response = requests.get(post.url)
        if response.status_code == 200:
            with open(os.path.join(output_dir, post.id + '.jpg'), 'wb') as img_f:
                img_f.write(response.content)