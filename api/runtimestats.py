from models.stats_model import RuntimeStats, RuntimeStatsSchema


def get_runtime_stats():
    """
    Responds to a request for GET /runtimestats.
    The responds contains all functions for which runtime stats are measured.
    :return:    the average runtime of the functions defined in
                configuration, in seconds.
    """
    stats_results = RuntimeStats.query.all()
    stats_schema = RuntimeStatsSchema(many=True)
    data = stats_schema.dump(stats_results)

    return data
