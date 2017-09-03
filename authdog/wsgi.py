import sys

import app

from pecan import conf
from pecan.deploy import deploy

from eventlet import wsgi
import eventlet


def main(conf_path):
    application = deploy(conf_path)

    eventlet_enabled = dict(conf.EVENTLET).get("enabled")
    if eventlet_enabled:
        eventlet.monkey_patch(time=True, thread=True)

    server_conf = dict(conf.server)
    port = int(server_conf.get("port"))
    host = server_conf.get("host")
    wsgi.server(eventlet.listen((host, port)), application)


if __name__ == "__main__":
    """Start server in this way when develop
    python authdog/wsgi.py  config.py
    """
    conf_path = sys.argv[1]
    main(conf_path)
