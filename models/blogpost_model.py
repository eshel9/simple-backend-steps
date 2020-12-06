from datetime import datetime
from bootstrap import db, ma


class BlogPost(db.Model):
    __tablename__ = 'blogpost'

    id = db.Column(db.Integer, primary_key='True')
    title = db.Column(db.String)
    body = db.Column(db.String)
    creator = db.Column(db.String)
    creation_timestamp = db.Column(db.String, default=datetime.utcnow)
    

class BlogPostSchema(ma.Schema):
    class Meta:
        model = BlogPost
        sqla_session = db.session
