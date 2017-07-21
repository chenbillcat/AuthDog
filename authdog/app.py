from pecan import make_app

import eventlet

from authdog import model


def setup_app(config):

    model.init_model()
    app_conf = dict(config.app)

    eventlet_enabled = dict(config.EVENTLET).get("enabled")

    if eventlet_enabled:
        eventlet.monkey_patch(time=True, thread=True)

    return make_app(
        app_conf.pop('root'),
        logging=getattr(config, 'logging', {}),
        **app_conf
    )
