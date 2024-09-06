import time
import threading

from metrics_decorator import metrics_collector
from db import init_db

SAVE_METRICS_PERIOD_SECS = 5


@metrics_collector
def example_function(secs):
    time.sleep(secs)
    if secs == 1:
        raise Exception("mock error")


@metrics_collector
def my_function(secs):
    time.sleep(secs)
    if secs == 1:
        raise Exception("mock error")


def save_metrics_period():
    while True:
        time.sleep(SAVE_METRICS_PERIOD_SECS)
        metrics_collector.save_metrics()


if __name__ == "__main__":
    init_db()

    threading.Thread(target=save_metrics_period).start()

    example_function(1)
    example_function(2)
    example_function(1)
    example_function(3)

    my_function(1)
    my_function(1)
    my_function(2)

    # -----------------
    example_function(1)
    example_function(3)

    my_function(1)
    my_function(2)
    my_function(1)
