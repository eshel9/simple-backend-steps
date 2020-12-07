from flask import make_response
from bootstrap import db
from models.blogpost_model import BlogPost, BlogPostSchema
from sqlalchemy import func, desc
from utils import static_var
from configuration import get_posts_size, top_creators_limit
from api.runtimestats import RuntimeRecorder
import json


# handler for POST /post
def create_new_post(blogpost):
    """
    Creates new blogpost based on user's request for POST /blogsposts
    Note that input validation is done automatically by swagger, by the standards defined in swagger.yml
    """
    with RuntimeRecorder('create_new_post'):
        schema = BlogPostSchema()
        print("the json blogpost that came from user is:", blogpost)
        new_blogpost = schema.load(blogpost, session=db.session)
        print(new_blogpost)

        db.session.add(new_blogpost)
        db.session.commit()

        return make_response(f"blogpost successfully created", 201)


# handler for GET /posts
@static_var("current_offset", 0)
def get_bunch_of_posts():
    """
    Responds to a request for GET /blogsposts
    :return:        list of a predetermined size of blogposts, sorted by
    creation time
    """
    with RuntimeRecorder('get_bunch_of_posts'):
        get_bunch_of_posts.current_offset += get_posts_size
        if get_bunch_of_posts.current_offset >= number_of_posts():
            get_bunch_of_posts.current_offset = 0

        blogposts_query = BlogPost.query.order_by(BlogPost.creation_timestamp)
        blogposts_query = blogposts_query.limit(get_posts_size)
        blogposts_query = blogposts_query.offset(get_bunch_of_posts.current_offset)
        blogposts = blogposts_query.all()

        # TODO currently sends all posts, send only a bunch
        blogpost_schema = BlogPostSchema(many=True)
        data = blogpost_schema.dump(blogposts)

        return data


# handler for GET /postsnumber
def get_number_of_posts():
    """
    Responds to a request for GET /postsnumber
    :return:        number of posts in the system
    """
    return make_response(
        f"the total number of posts is: {number_of_posts()}", 200
    )


def number_of_posts():
    query_result = db.session.query(func.count(BlogPost.id)).first()
    return int(query_result[0])


# handler for GET /postsnumber
def get_top_creators():
    """
    Responds to a request for GET /postsnumber
    :return:        number of posts in the system
    """
    query = db.session.query(BlogPost.creator, func.count(BlogPost.creator))
    query = query.group_by(BlogPost.creator)
    query = query.order_by(desc(func.count(BlogPost.creator)))
    query_results = query.limit(top_creators_limit).all()

    # convert results from a list of values to a list of dictionaries with
    # titles to each value, same format as with posts
    results = []
    for query_result in query_results:
        results += [{"creator": query_result[0],
                    "number_of posts:": query_result[1]}]

    data = json.dumps(results, indent=4)

    return make_response(
        data, 200
    )

