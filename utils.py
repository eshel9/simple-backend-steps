from sqlalchemy import func
from bootstrap import db
from models.blogpost_model import BlogPost


def static_var(variable_name, value):
    def decorate(function):
        setattr(function, variable_name, value)
        return function

    return decorate


def number_of_posts():
    query_result = db.session.query(func.count(BlogPost.id)).first()
    return int(query_result[0])
