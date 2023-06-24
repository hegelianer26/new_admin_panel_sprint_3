from loggings import logger
from elasticsearch import Elasticsearch
from configs import etl_settings
from decorators import backoff


MAPPING_FOR_INDEX = {
    "dynamic": "strict",
    "properties": {
      "id": {
        "type": "keyword"
      },
      "imdb_rating": {
        "type": "float"
      },
      "genre": {
        "type": "keyword"
      },
      "title": {
        "type": "text",
        "analyzer": "ru_en",
        "fields": {
          "raw": {
            "type":  "keyword"
          }
        }
      },
      "description": {
        "type": "text",
        "analyzer": "ru_en"
      },
      "director": {
        "type": "text",
        "analyzer": "ru_en",
      },
      "actors_names": {
        "type": "text",
        "analyzer": "ru_en"
      },
      "writers_names": {
        "type": "text",
        "analyzer": "ru_en"
      },
      "actors": {
        "type": "nested",
        "dynamic": "strict",
        "properties": {
          "id": {
            "type": "keyword"
          },
          "name": {
            "type": "text",
            "analyzer": "ru_en"
          }
        }
      },
      "writers": {
        "type": "nested",
        "dynamic": "strict",
        "properties": {
          "id": {
            "type": "keyword"
          },
          "name": {
            "type": "text",
            "analyzer": "ru_en"
          }
        }
      }
    }
  }
ES_SETTINGS = {
    "refresh_interval": "1s",
    "analysis": {
      "filter": {
        "english_stop": {
          "type":       "stop",
          "stopwords":  "_english_"
        },
        "english_stemmer": {
          "type": "stemmer",
          "language": "english"
        },
        "english_possessive_stemmer": {
          "type": "stemmer",
          "language": "possessive_english"
        },
        "russian_stop": {
          "type":       "stop",
          "stopwords":  "_russian_"
        },
        "russian_stemmer": {
          "type": "stemmer",
          "language": "russian"
        }
      },
      "analyzer": {
        "ru_en": {
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "english_stop",
            "english_stemmer",
            "english_possessive_stemmer",
            "russian_stop",
            "russian_stemmer"
          ]
        }
      }
    }
  }


class ElasticSearchConnection:
    start_sleep_time = etl_settings.start_sleep_time
    factor = etl_settings.factor
    border_sleep_time = etl_settings.border_sleep_time

    def __init__(self):
        self.my_connection = None
        self.ping = False
        self._connect()

    @backoff
    def _connect(self):
        self.my_connection = Elasticsearch('http://172.17.0.1:9200/')
        logger.info(
            'Соединение с Elasticsearch: %s', self.my_connection.ping())
        if not self.my_connection.ping():
            self.my_connection = Elasticsearch('http://172.17.0.1:9200/')
            raise ConnectionRefusedError

    @backoff
    def create_index(self, index):
        if self.my_connection.indices.exists(index=index):
            pass
        self.my_connection.indices.create(
            index=index, settings=ES_SETTINGS, mappings=MAPPING_FOR_INDEX)
        logger.info('Индекс %s создан', index)

    @backoff
    def __del__(self):
        self.my_connection.close
        logger.info('Соединение с ElasticSearch закрыто')
