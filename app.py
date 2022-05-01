from threading import Thread
from time import sleep

from schedule import every, run_pending
from services import (
    index_latest_cnn_rss_feed_entries,
    scrape_cnn_rss_feeds_page,
    scrape_latest_cnn_articles
)

from src import app, ServiceContainer


c = ServiceContainer(index_latest_cnn_rss_feed_entries)
every(15).minutes.do(c.run, params={})

c = ServiceContainer(scrape_cnn_rss_feeds_page)
every(1).day.do(c.run)

c = ServiceContainer(scrape_latest_cnn_articles)
# every(15).minutes.do(c.run)


@app.route('/endpoints')
def endpoints():
    return {'endpoints': [str(e) for e in app.url_map.iter_rules() if str(e) != "/static/<path:filename>"]}


def run_flask():
    app.run(port=8080)


def run_scheduler():
    while True:
        run_pending()
        sleep(1)


if __name__ == '__main__':
    t1 = Thread(target=run_flask, daemon=True)
    t2 = Thread(target=run_scheduler, daemon=True)

    for t in [t1, t2]:
        t.start()

    while True:
        sleep(12*60*60)
