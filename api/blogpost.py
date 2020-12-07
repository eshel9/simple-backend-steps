from flask import make_response
from bootstrap import db
from models.blogpost_model import BlogPost, BlogPostSchema
from sqlalchemy import func, desc
from utils import static_var, number_of_posts
from project_configuration.configuration import get_posts_size, top_creators_limit
from api.runtimestats import RuntimeRecorder
import json


def create_new_post(blogpost):
    """
    Creates new blogpost based on user's request for POST /blogsposts
    Note that input validation is done automatically by swagger,
    by the standards defined in api_configuration.yml
    Note: this function's runtime is recorded and saved to the DB for stats querying
    """
    with RuntimeRecorder('create_new_post'):
        schema = BlogPostSchema()
        new_blogpost = schema.load(blogpost, session=db.session)

        db.session.add(new_blogpost)
        db.session.commit()

        return make_response(f"blogpost successfully created", 201)


@static_var("current_offset", 0)
def get_bunch_of_posts():
    """
    Responds to a request for GET /blogsposts
    Note: this function's runtime is recorded and saved to the DB for stats querying
    :return:        list of a predetermined size of blogposts, sorted by
    creation time
    """
    with RuntimeRecorder('get_bunch_of_posts'):
        # remember the indexes of the last bunch we sent,
        # to be able to send the next bunch
        get_bunch_of_posts.current_offset += get_posts_size
        if get_bunch_of_posts.current_offset >= number_of_posts():
            get_bunch_of_posts.current_offset = 0

        blogposts_query = BlogPost.query.order_by(BlogPost.creation_timestamp)
        blogposts_query = blogposts_query.limit(get_posts_size)
        blogposts_query = blogposts_query.offset(get_bunch_of_posts.current_offset)
        blogposts = blogposts_query.all()

        blogpost_schema = BlogPostSchema(many=True)
        data = blogpost_schema.dump(blogposts)

        return data


def get_number_of_posts():
    """
    Responds to a request for GET /postsnumber
    :return:        number of posts in the system
    """
    return make_response(f"the total number of posts is: {number_of_posts()}", 200)


def get_top_creators():
    f"""
    Responds to a request for GET /topcreators
    :return:        list of size {top_creators_limit} of the creators with the most posts
    """
    query = db.session.query(BlogPost.creator, func.count(BlogPost.creator))
    query = query.group_by(BlogPost.creator)
    query = query.order_by(desc(func.count(BlogPost.creator)))
    query_results = query.limit(top_creators_limit).all()

    # since there is no schema for creators, convert results to the same format as with posts.
    # [(name, number)] -> [{"creator": name, "number": number}]
    results = []
    for query_result in query_results:
        results += [{"creator": query_result[0],
                     "number_of posts:": query_result[1]}]

    data = json.dumps(results, indent=4)

    return make_response(data, 200)
