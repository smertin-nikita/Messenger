import time
from datetime import datetime
from flask import Flask, request, Response

# test_config: write what is this?!
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

db = []


@app.route('/')
def index():
    return "Messenger<br><a href='/status'>Status</a>"


@app.route("/send_message", methods=['POST'])
def send_message():
    data = request.json
    if not isinstance(data, dict):
        return Response('error', 400)
    text = data.get('text')
    author = data.get('author')
    if isinstance(text, str) and isinstance(author, str):
        db.append({
            'text': text,
            'author': author,
            'time': time.time()
        })
        return Response('ok')
    else:
        return Response('wrong format', 400)


@app.route("/get_messages")
def get_messages():
    after = request.args.get('after', '0')
    try:
        after = float(after)
    except:
        return Response('wrong format', 400)
    # Get all messages where message time > after
    new_messages = [n for n in db if n['time'] > after]
    return {'messages', new_messages}


@app.route("/status")
def status():
    dn = datetime.now()
    # Get set of authors
    authors = set([n['author'] for n in db])
    return {
        "status": True,
        "name": "Messenger",
        "authors_cnt": len(authors),
        "messages_cnt": len(db),
        "time": str(dn.strftime('%Y-%m-%d %H:%M'))
    }


app.run()
