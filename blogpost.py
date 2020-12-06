from datetime import datetime
from flask import make_response, abort
from bootstrap import db
from models.blogpost_model import BlogPost, BlogPostSchema
from sqlalchemy import func
from utils import static_var
from configuration import get_posts_size


# handler for POST /post
def create_new_post(blogpost):
    """
    Creates new blogpost based on user's request for POST /blogsposts
    """
    schema = BlogPostSchema()
    print("the json blogpost that came from user is:", blogpost)
    new_blogpost = schema.load(blogpost, session=db.session)
    print(new_blogpost)

    db.session.add(new_blogpost)
    db.session.commit()

    return make_response(
        f"blogpost successfully created", 201
    )


# handler for GET /posts
@static_var("current_offset", 0)
def get_bunch_of_posts():
    """
    Responds to a request for GET /blogsposts
    :return:        list of a predetermined size of blogposts, sorted by
    creation time
    """
    # TODO record runtime
    get_bunch_of_posts.current_offset += get_posts_size
    if get_bunch_of_posts.current_offset >= number_of_posts():
        get_bunch_of_posts.current_offset = 0

    blogposts_query = BlogPost.query.order_by(BlogPost.creation_timestamp)
    blogposts_query = blogposts_query.limit(get_posts_size)
    blogposts_query = blogposts_query.offset(get_bunch_of_posts.current_offset)
    blogposts = blogposts_query.all()

    for i in blogposts:
        print(i, i.id, i.title, i.creator, i.body)

    # TODO currently sends all posts, send only a bunch
    blogpost_schema = BlogPostSchema(many=True)
    data = blogpost_schema.dump(blogposts)
    print(data)
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

