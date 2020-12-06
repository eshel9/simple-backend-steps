from datetime import datetime
from flask import make_response, abort
from bootstrap import db
from models.blogpost_model import BlogPost, BlogPostSchema


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


# handler for GET /posts
def get_bunch_of_posts():
    """
    Responds to a request for GET /blogsposts
    :return:        list of a predetermined size of blogposts, sorted by
    creation time
    """
    return [BLOGPOSTS[key] for key in sorted(BLOGPOSTS.keys())]


# handler for POST /post
def create_new_post(blogpost):
    """
    Creates new blogpost based on user's request for POST /blogsposts
    """
    current_blogpost_id = len(BLOGPOSTS) + 1

    BLOGPOSTS[current_blogpost_id] = {
        "title": blogpost["title"],
        "body": blogpost["body"],
        "creator": blogpost["creator"],
        "timestamp": get_timestamp(),
    }
    return make_response(
        f"{current_blogpost_id} successfully created", 201
    )


# handler for GET /postsnumber
def get_number_of_posts():
    """
    Responds to a request for GET /postsnumber
    :return:        number of posts in the system
    """
    return make_response(
        f"there are currently {len(BLOGPOSTS)} posts in the system", 200
    )
