from models.stats_model import RuntimeStats, RuntimeStatsSchema
from contextlib import AbstractContextManager
from timeit import default_timer as timer
from bootstrap import db


# handler for GET /runtimestats
def get_runtime_stats():
    """
    Responds to a request for GET /blogsposts
    :return:  the average runtime of the functions defined in configuration
    """
    stats_results = RuntimeStats.query.all()

    # TODO currently sends all posts, send only a bunch
    stats_schema = RuntimeStatsSchema(many=True)
    data = stats_schema.dump(stats_results)

    return data


class RuntimeRecorder(AbstractContextManager):
    """This class is used in functions for which we are concerned with runtime.
    Its context's runtime will be measured and recorded in the DB"""
    def __init__(self, function_name):
        self.function_name = function_name
        self.start_time = None
        self.exit_time = None

    def __enter__(self):
        self.start_time = timer()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.exit_time = timer()
        elapsed_time = self.exit_time - self.start_time

        # increment the call_times property of this function's runtimestat
        stats_query = RuntimeStats.query.filter_by(function_name=self.function_name)
        stats_result = stats_query.first()
        stats_result.call_times += 1

        updated_average = self._weighted_average(stats_result.runtime_avg,
                                                 stats_result.call_times, elapsed_time)

        stats_result.runtime_avg = updated_average
        db.session.add(stats_result)
        db.session.commit()

    def _weighted_average(self, first_value, first_weight, second_value):
        # second_weight equals 1
        total = (first_value * first_weight) + second_value
        return total / (first_weight + 1)
