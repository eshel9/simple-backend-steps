from bootstrap import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class RuntimeStats(db.Model):
    __tablename__ = 'runtimestats'

    id = db.Column(db.Integer, primary_key='True')
    function_name = db.Column(db.String)
    runtime_avg = db.Column(db.Float)
    call_times = db.Column(db.Integer)
    

class RuntimeStatsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = RuntimeStats
        include_fk = False
        load_instance = True
