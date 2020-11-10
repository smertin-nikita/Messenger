import time
import os

from datetime import datetime
from flask import Flask, request, Response


# test_config: write what is this?!
def create_app(test_config=None):
    # create and configure the app. Relative to the instance path
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # start page
    @app.route('/')
    def index():
        return "Messenger<br><a href='/status'>Status</a>"

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    return app

#
# @app.route("/send_message", methods=['POST'])
# def send_message():
#     data = request.json
#     if not isinstance(data, dict):
#         return Response('error', 400)
#     text = data.get('text')
#     author = data.get('author')
#     if isinstance(text, str) and isinstance(author, str):
#         db.append({
#             'text': text,
#             'author': author,
#             'time': time.time()
#         })
#         return Response('ok')
#     else:
#         return Response('wrong format', 400)
#
#
# @app.route("/get_messages")
# def get_messages():
#     after = request.args.get('after', '0')
#     try:
#         after = float(after)
#     except:
#         return Response('wrong format', 400)
#     # Get all messages where message time > after
#     new_messages = [n for n in db if n['time'] > after]
#     return {'messages', new_messages}
#
#
# @app.route("/status")
# def status():
#     dn = datetime.now()
#     # Get set of authors
#     authors = set([n['author'] for n in db])
#     return {
#         "status": True,
#         "name": "Messenger",
#         "authors_cnt": len(authors),
#         "messages_cnt": len(db),
#         "time": str(dn.strftime('%Y-%m-%d %H:%M'))
#     }
#
#
# app.run()
