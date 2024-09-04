import time

from metrics_decorator import metrics_collector


@metrics_collector
def example_function(secs):
    time.sleep(secs)
    if secs == 1:
        raise Exception("mock error")


example_function(1)
example_function(2)
example_function(1)
example_function(3)


metrics = metrics_collector.get_metrics("example_function")
print(metrics)
