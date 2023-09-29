from states import State, JsonFileStorage
from datetime import datetime
from postgres_from import PostgresConnection
from elastic_to import ElasticSearchConnection
from configs import etl_settings, elastic_setings
from loggings import logger
from elasticsearch.helpers import streaming_bulk
from threading import Timer
from sql_queries import big_sql_query, small_sql_query


def get_time():
    time_dirty = my_storage.get_state('Movies')
    time = datetime.strptime(time_dirty, "%Y-%m-%d %H:%M:%S.%f%z")
    return time


def set_time(time_object):
    dt_str = time_object.strftime("%Y-%m-%d %H:%M:%S.%f%z")
    my_storage.set_state('Movies', dt_str)


def check_needs(db,  query):
    updated = get_time()
    data = db.extract_data(query, updated, 1)
    for i in data:
        return i[0]


def extract(db, query):
    updated = get_time()
    data = db.extract_data(query, updated, etl_settings.batch_size)
    logger.info(
        'Выгружено %d фильмов', len(data))
    return data


def transform(data):
    for row in data:
        doc = {
            "_id": row["id"],
            "id": row["id"],
            "imdb_rating": row["imdb_rating"],
            "genre_names": row["genre_names"],
            "genre": row["genre"],
            "title": row["title"],
            "description": row["description"],
            "director_name": row["director_name"],
            "actors_names": [row["actors_names"]],
            "writers_names": [row["writers_names"]],
            "actors": row["actors"],
            "writers":  row["writers"],
            "director":  row["director"],
        }
        yield doc


def load(data):
    successes = 0
    if data:
        elastic = ElasticSearchConnection()
        elastic.create_index(elastic_setings.index)
        for ok, action in streaming_bulk(client=elastic.my_connection,
                                         index=elastic_setings.index, actions=transform(data)
                                         ):
            successes += ok
            logger.info("Indexed %d documents" % (successes))
        set_time(time_object=data[0]['great'])

    else:
        logger.info(
            'Elasticseach в актуальном состоянии, загрузки не требуются')


if __name__ == '__main__':

    my_storage = State(
        JsonFileStorage(file_path=etl_settings.storage_file_path))

    def f():
        logger.info('начало etl')
        db = PostgresConnection()
        Timer(etl_settings.timer, f).start()
        if check_needs(db, small_sql_query) > get_time():
            logger.info('начало загрузки')
            load(extract(db, big_sql_query))
        else:
            logger.info(
                'Elasticseach в актуальном состоянии, обновлений не найдено')
        logger.info('завершение etl')
    f()
