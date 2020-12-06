from datetime import datetime


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


# Sample Data to serve with our API
BLOGPOSTS = {
    "1": {
        "title": "Weather",
        "creator": "Farrell",
        "body": "Such a nice weather today!",
        "creation_timestamp": get_timestamp()
    },
    "2": {
        "title": "First Post",
        "creator": "Will",
        "body": "Hello everybody, this is my first post",
        "creation_timestamp": get_timestamp()
    },
    "3": {
        "title": "New clothes",
        "creator": "Doug",
        "body": "What do you think about my new clothes?",
        "creation_timestamp": get_timestamp()
    }
}


# handler for GET blogpost
def test():
    """
    This function responds to a request for /blogsposts
    :return:        sorted list of blogposts
    """
    return [BLOGPOSTS[key] for key in sorted(BLOGPOSTS.keys())]
