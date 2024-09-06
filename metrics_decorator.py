import time
from datetime import datetime

from db import save_metric


class MetricCollector:
    def __init__(self):
        self.metrics = {}

    def __call__(self, func):
        def wrapper(*args):
            if self.metrics.get(func.__name__) is None:
                self.metrics[func.__name__] = {
                    "num_calls": 0,
                    "num_errors": 0,
                    "avg_exec_time": 0,
                    "total_exec_time": 0,
                }

            try:
                start = time.time()
                func(*args)
            except Exception:
                self.metrics[func.__name__]["num_errors"] += 1
            finally:
                self.metrics[func.__name__]["num_calls"] += 1
                self.metrics[func.__name__]["total_exec_time"] += time.time() - start
                self.metrics[func.__name__]["avg_exec_time"] = (
                    self.metrics[func.__name__]["total_exec_time"]
                    / self.metrics[func.__name__]["num_calls"]
                )

        return wrapper

    def get_metrics(self, func_name):
        metric = self.metrics.get(func_name)
        num_calls = metric["num_calls"] if metric else 0
        avg_exec_time = metric["avg_exec_time"] if metric else 0
        num_errors = metric["num_errors"] if metric else 0

        return (
            f"Function: {func_name}\n"
            f"Number of calls: {num_calls}\n"
            f"Average execution time: {avg_exec_time} seconds\n"
            f"Number of errors: {num_errors}"
        )

    def save_metrics(self):
        print("::save_metrics", self.metrics)

        metric_list = []
        for key, val in self.metrics.items():
            if val.get("num_calls") == 0:
                continue

            metric_list.append(
                (
                    key,
                    val.get("num_calls"),
                    val.get("num_errors"),
                    val.get("avg_exec_time"),
                    datetime.now(),
                )
            )

            self.metrics[key] = {
                "num_calls": 0,
                "num_errors": 0,
                "avg_exec_time": 0,
                "total_exec_time": 0,
            }

        if not metric_list:
            return

        save_metric(metric_list)


metrics_collector = MetricCollector()
