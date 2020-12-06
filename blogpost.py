from datetime import datetime
from flask import make_response, abort
from bootstrap import db
from models.blogpost_model import BlogPost, BlogPostSchema
from sqlalchemy import func
from configuration import get_posts_size


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


# handler for POST /post
def create_new_post(blogpost):
    """
    Creates new blogpost based on user's request for POST /blogsposts
    """
    schema = BlogPostSchema()
    new_blogpost = schema.load(blogpost, session=db.session)

    db.session.add(new_blogpost)
    db.session.commit()

    return make_response(
        f"blogpost successfully created", 201
    )


# handler for GET /posts
def get_bunch_of_posts():
    """
    Responds to a request for GET /blogsposts
    :return:        list of a predetermined size of blogposts, sorted by
    creation time
    """
    # TODO record runtime
    blogposts = BlogPost.query.order_by(BlogPost.creation_timestamp).all()
    print(blogposts)
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
    number_of_posts = BlogPost.query(func.count(BlogPost.id))
    print("number of posts:", number_of_posts)
    return make_response(
        f"there are currently {number_of_posts} posts in the system", 200
    )
