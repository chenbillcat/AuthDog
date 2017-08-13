# Server Specific Configurations
server = {
    'port': '8080',
    'host': '0.0.0.0'
}

# Pecan Application Configurations
app = {
    'root': 'authdog.controllers.root.RootController',
    'modules': ['authdog'],
    'static_root': '%(confdir)s/../../public',
    'template_path': '%(confdir)s/../templates',
    'debug': True,
    'errors': {
        '404': '/error/404',
        '__force_dict__': True
    }
}

logging = {
    'root': {'level': 'INFO', 'handlers': []},
    'loggers': {
        'authdog': {'level': 'DEBUG', 'handlers': ['applogfile'], 'propagate': False},
        'pecan': {'level': 'DEBUG', 'handlers': [], 'propagate': False},
        'py.warnings': {'handlers': []},
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
# Custom Configurations must be in Python dictionary format::
#
# foo = {'bar':'baz'}
#
# All configurations are accessible at::
# pecan.conf

# Bindings and options to pass to SQLAlchemy's ``create_engine``
sqlalchemy = {
    'url': 'mysql+pymysql://root:qazwsx@localhost:3306/test',
    'echo': False,
    'echo_pool': False,
    'pool_recycle': 3600,
    'encoding': 'utf-8'
}
