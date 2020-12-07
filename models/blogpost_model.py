from datetime import datetime
from bootstrap import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class BlogPost(db.Model):
    __tablename__ = 'blogpost'

    id = db.Column(db.Integer, primary_key='True')
    title = db.Column(db.String)
    body = db.Column(db.String)
    creator = db.Column(db.String)
    creation_timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class BlogPostSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = BlogPost
        include_relationships = True
        load_instance = True
