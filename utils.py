import datetime
import random

def randomDateGenerator():
    start = datetime.datetime(2017, 1, 1, 0, 0, 0)
    end = datetime.datetime.now()
    return start + datetime.timedelta(
        # Get a random amount of seconds between `start` and `end`
        seconds=random.randint(0, int((end - start).total_seconds())),
    )
