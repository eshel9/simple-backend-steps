#! ./backend-env/bin/python
import os
from bootstrap import initialize_backend

initialize_backend()

from models.blogpost_model import BlogPost
from models.stats_model import RuntimeStats
from bootstrap import db, dbname


BASE_POSTS = [
    {'title': 'title1', 'body': 'body1', 'creator': 'creator1'},
    {'title': 'title2', 'body': 'body2', 'creator': 'creator2'},
    {'title': 'title3', 'body': 'body3', 'creator': 'creator3'},
    {'title': 'title4', 'body': 'body4', 'creator': 'creator4'},
]

BASE_RUNTIMES = [
    {'function_name': 'create_new_post', 'runtime_avg': 0, 'call_times':
        0},
    {'function_name': 'get_number_of_posts', 'runtime_avg': 0, 'call_times':
        0},
]

if os.path.exists(dbname):
    os.remove(dbname)

db.create_all()

for post in BASE_POSTS:
    post_object = BlogPost(creator=post['creator'], title=post['title'],
                           body=post['body'])
    db.session.add(post_object)

for post in BASE_RUNTIMES:
    runtime_object = RuntimeStats(function_name=post['function_name'],
                                  runtime_avg=post['runtime_avg'],
                                  call_times=post['call_times'])
    db.session.add(runtime_object)

db.session.commit()
