from src import app, register
from services import SERVICES

for func in SERVICES:
    register(func)

if __name__ == '__main__':
    app.run(port=8080)
