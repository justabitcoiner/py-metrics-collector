import time
import multiprocessing

from metrics_decorator import metrics_collector
from db import init_db


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


if __name__ == "__main__":
    init_db()
    multiprocessing.set_start_method("spawn")

    example_function(1)
    example_function(2)
    example_function(1)
    example_function(3)

    my_function(1)
    my_function(1)
    my_function(2)

    metrics = metrics_collector.get_metrics("example_function")
    print(metrics)
    metrics = metrics_collector.get_metrics("my_function")
    print(metrics)

    metrics_collector.save_metrics_in_background()

    # -----------------
    example_function(1)
    example_function(3)

    my_function(1)
    my_function(2)
    my_function(1)

    metrics = metrics_collector.get_metrics("example_function")
    print(metrics)
    metrics = metrics_collector.get_metrics("my_function")
    print(metrics)

    metrics_collector.save_metrics_in_background()
