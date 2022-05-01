from src import app, ServiceContainer
from services import SERVICES

for service in SERVICES:
    ServiceContainer(service)


@app.route('/endpoints')
def endpoints():
    return {'endpoints': [s.__name__.replace('_', '-') for s in SERVICES]}


if __name__ == '__main__':
    app.run(port=8080)
