from flask import make_response
from datetime import datetime


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


# Sample Data to serve with our API
BLOGPOSTS = {
    1: {
        "title": "Weather",
        "creator": "Farrell",
        "body": "Such a nice weather today!",
        "creation_timestamp": get_timestamp()
    },
    2: {
        "title": "First Post",
        "creator": "Will",
        "body": "Hello everybody, this is my first post",
        "creation_timestamp": get_timestamp()
    },
    3: {
        "title": "New clothes",
        "creator": "Doug",
        "body": "What do you think about my new clothes?",
        "creation_timestamp": get_timestamp()
    }
}


# handler for GET blogpost
def get_bunch_of_posts():
    """
    This function responds to a request for GET /blogsposts
    
    :return:        sorted list of blogposts
    """
    return [BLOGPOSTS[key] for key in sorted(BLOGPOSTS.keys())]


# handler for POST blogpost
def create_new_post(blogpost):
    """
    This function responds to a request for POST /blogsposts
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
