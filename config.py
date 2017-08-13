# Server Specific Configurations
server = {
    'port': '8080',
    'host': '0.0.0.0'
}

# Pecan Application Configurations
app = {
    'root': 'authdog.controllers.root.RootController',
    'modules': ['authdog'],
    'static_root': '%(confdir)s/public',
    'template_path': '%(confdir)s/authdog/templates',
    'debug': True,
    'errors': {
        404: '/error/404',
        '__force_dict__': True
    }
}

logging = {
    'root': {'level': 'INFO', 'handlers': ['console']},
    'loggers': {
        'authdog': {'level': 'DEBUG', 'handlers': ['applogfile'], 'propagate': False},
        'pecan': {'level': 'DEBUG', 'handlers': ['console'], 'propagate': False},
        'py.warnings': {'handlers': ['console']},
        '__force_dict__': True
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'color'
        },
        'applogfile':{
            'level': 'DEBUG',
            #'class': 'logging.FileHandler',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'color',
            'filename': '/var/log/authdog/authdog.log',
            'backupCount': 5
        }
    },
    'formatters': {
        'simple': {
            'format': ('%(asctime)s %(levelname)-5.5s [%(name)s]'
                       '[%(threadName)s] %(message)s')
        },
        'color': {
            '()': 'pecan.log.ColorFormatter',
            'format': ('%(asctime)s :: %(levelname)s :: %(name)s '
                       ':: %(threadName)s :: %(message)s'),
            '__force_dict__': True
        }
    }
}

SECREATE_KEY = "capsCrmRong"
EVENTLET = {'enabled': True}
# Custom Configurations must be in Python dictionary format::
#
# foo = {'bar':'baz'}
#
# All configurations are accessible at::
# pecan.conf
