from abc import ABC, abstractmethod

from schedule import Job


class FlowContainer(ABC):
    def __init__(self, run_interval: Job = None):
        self.run_interval = run_interval
        self.is_scheduled = run_interval is not None

        if self.is_scheduled:
            self.run_interval.do(self.run)

    @abstractmethod
    def run(self):
        pass
