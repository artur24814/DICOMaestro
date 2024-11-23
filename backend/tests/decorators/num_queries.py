from django.db import connection
from django.test.utils import CaptureQueriesContext
from functools import wraps


def assert_num_queries(expected_num_queries):
    def decorator(test_func):
        @wraps(test_func)
        def wrapper(*args, **kwargs):
            with CaptureQueriesContext(connection) as context:
                result = test_func(*args, **kwargs)
                num_queries = len(context.captured_queries)
                assert num_queries <= expected_num_queries, (
                    f"The number of database queries did not match. "
                    f"It was expected that no more than that: {expected_num_queries}, "
                    f"executed: {num_queries}.\n"
                    f"Queries: {context.captured_queries}"
                )
                return result
        return wrapper
    return decorator
