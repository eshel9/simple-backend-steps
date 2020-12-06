from bootstrap import db, ma


class RuntimeStats(db.Model):
    __tablename__ = 'runtimestats'

    id = db.Column(db.Integer, primary_key='True')
    function_name = db.Column(db.String)
    runtime_avg = db.Column(db.Float)
    call_times = db.Column(db.Integer)
    

class RuntimeStatsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RuntimeStats
        include_fk = False
