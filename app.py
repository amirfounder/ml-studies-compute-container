from threading import Thread
from time import sleep

import schedule

from src.models.service_container import ServiceContainer, ServiceContainers as Containers
from src import app
from services import SERVICES

for service in SERVICES:
    ServiceContainer(service)


schedule.every(15).minutes.do(Containers.containers.get('index_latest_cnn_rss_feed_entries').run, params={})


@app.route('/endpoints')
def endpoints():
    return {'endpoints': [s.__name__.replace('_', '-') for s in SERVICES]}


if __name__ == '__main__':
    def run_scheduler():
        while True:
            schedule.run_pending()
            sleep(1)
    t = Thread(target=run_scheduler, daemon=True)
    t.start()
    app.run(port=8080)
