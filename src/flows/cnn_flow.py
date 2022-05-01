import schedule

from src.models.flow_container import FlowContainer


class CnnFlow(FlowContainer):
    super().__init__(
        run_interval=schedule.every(10).minutes
    )

    def run(self):
        pass
