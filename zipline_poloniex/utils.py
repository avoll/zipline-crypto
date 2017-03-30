# -*- coding: utf-8 -*-
"""
Additional utilities
"""
import time
import logging
import functools
from math import fabs
from datetime import datetime

from pytz import timezone

__author__ = "Florian Wilhelm"
__copyright__ = "Florian Wilhelm"
__license__ = "new-bsd"

_logger = logging.getLogger(__name__)


def unix_time(dt):
    """Convert datetime to seconds since epoch

    Args:
        dt: datetime object

    Returns:
        seconds since epoch
    """
    epoch = datetime.utcfromtimestamp(0).replace(tzinfo=timezone('UTC'))
    dt = dt.replace(tzinfo=timezone('UTC'))
    return (dt - epoch).total_seconds()


def throttle(calls, seconds=1):
    """Decorator for throttling a function to number of calls per seconds

    Args:
        calls (int): number of calls in interval
        seconds (int): number of seconds in interval

    Returns:
        wrapped function
    """
    assert isinstance(calls, int), 'number of calls must be integer'
    assert isinstance(seconds, int), 'number of seconds must be integer'

    def wraps(func):
        # keeps track of the last calls
        last_calls = list()

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            curr_time = time.time()
            if last_calls:
                # remove calls from last_calls list older then period in seconds
                idx_old_calls = [i for i, t in enumerate(last_calls) if t < curr_time - seconds]
                if idx_old_calls:
                    del last_calls[:idx_old_calls[-1]]
            if len(last_calls) >= calls:
                idx = len(last_calls) - calls
                delta = fabs(1 - curr_time + last_calls[idx])
                print(delta)
                logger = logging.getLogger(func.__module__)
                logger.debug("Throttling function {}".format(func.__name__))
                time.sleep(delta)
            resp = func(*args, **kwargs)
            last_calls.append(time.time())
            return resp

        return wrapper

    return wraps
