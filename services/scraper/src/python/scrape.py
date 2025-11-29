import json
import os
from datetime import datetime
from facebook_scraper import get_posts

group_id = os.environ.get('SCRAPER_GROUP_ID')
email = os.environ.get('SCRAPER_EMAIL')
password = os.environ.get('SCRAPER_PASSWORD')

if not group_id:
    raise SystemExit('SCRAPER_GROUP_ID is required')

def serialize(post):
    return {
        'source': {
            'platform': 'facebook',
            'group_id': str(group_id),
            'post_id': str(post.get('post_id')),
            'url': post.get('post_url'),
        },
        'raw': {
            'text': post.get('text'),
            'html': None,
            'images': post.get('images') or [],
            'author_name': post.get('username'),
            'author_id': post.get('user_id'),
        },
        'posted_at': post.get('time').isoformat() if isinstance(post.get('time'), datetime) else None,
    }

posts = []
for post in get_posts(group=group_id, pages=1, credentials=(email, password)):
    posts.append(serialize(post))

print(json.dumps(posts))
