import os
import json

MAX_COMMENTS = '3000'
POSTS_FILE = 'r-EDAnonymous-Top 02-16-2020.json'

with open(POSTS_FILE) as posts_json:
    posts = json.load(posts_json)

    for post in posts.values():
        post_url = post['URL']
        print('Running command: ../.venv/bin/python ../scraper.py -c {post_url} {MAX_COMMENTS} --json')
        os.system(f'../.venv/bin/python ../scraper.py -c {post_url} {MAX_COMMENTS} --json')
