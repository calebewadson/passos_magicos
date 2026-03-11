import logging
from logging.config import dictConfig
from src.settings import LOG_DIR

def setup_logging():
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    dictConfig({
        'version':1,
        'disable_existing_loggers':False,
        'formatters':{
            'json':{
                '()':'pythonjsonlogger.jsonlogger.JsonFormatter',
                'fmt':'%(asctime)s %(levelname)s %(name)s %(message)s'
            },
            'standard':{
                'format':'%(asctime)s | %(levelname)s | %(name)s | %(message)s'
            }
        },
        'handlers':{
            'console':{
                'class':'logging.StreamHandler',
                'formatter':'standard',
                'level':'INFO'
            },
            'file':{
                'class':'logging.FileHandler',
                'formatter':'json',
                'filename':str(LOG_DIR/'app.log'),
                'encoding':'utf-8',
                'level':'INFO'
            }
        },
        'root':{
            'handlers':['console','file'],
            'level':'INFO'
        }
    })

def get_logger(name): return logging.getLogger(name)