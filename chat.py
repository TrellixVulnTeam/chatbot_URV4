import logging
import os
from dotenv import load_dotenv
from server import create_app, socketio

for file in [x.strip() for x in os.getenv('CONFIG_ENV', default='').split(',')]:
    load_dotenv(file)
print(os.environ.values())

logging.basicConfig(level=logging.WARNING)

app = create_app(debug=True)

if __name__ == '__main__':
    socketio.run(app)
