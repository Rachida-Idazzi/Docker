from flask import Flask
import redis

app = Flask(__name__)
client = redis.Redis(host='redis', port=6379, decode_responses=True)


@app.route('/')
def hello():
    return "Hello, World! Welcome to my Flask + Redis Lab!"

@app.route('/count')
def count():
    client.incr('hits')
    counter = client.get('hits')
    return f"This webpage has been viewed {counter} time(s)."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)