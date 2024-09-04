import time


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
                self.metrics[func.__name__]["num_calls"] += 1
                start = time.time()
                func(*args)
            except Exception:
                self.metrics[func.__name__]["num_errors"] += 1
            finally:
                self.metrics[func.__name__]["total_exec_time"] += time.time() - start
                self.metrics[func.__name__]["avg_exec_time"] = self.metrics[func.__name__]["total_exec_time"] / self.metrics[func.__name__]["num_calls"]

        return wrapper

    def get_metrics(self, func_name):
        return f"Function: {func_name} \nNumber of calls: {self.metrics[func_name]["num_calls"]} \nAverage execution time: {self.metrics[func_name]["avg_exec_time"]} seconds \nNumber of errors: {self.metrics[func_name]["num_errors"]}"


metrics_collector = MetricCollector()
