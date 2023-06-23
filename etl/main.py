from states import State, JsonFileStorage
from datetime import datetime
from postgres_from import PostgresConnection
from elastic_to import ElasticSearchConnection
from configs import etl_settings
from logging import getLogger, StreamHandler
from elasticsearch.helpers import streaming_bulk
from threading import Timer
from sql_queries import (
    sql_movies, sql_persons, sql_genres, sql_movie, sql_genre, sql_person)


logger = getLogger(__name__)
logger.addHandler(StreamHandler())
logger.setLevel("INFO")


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


def extract(db, query, table):
    updated = get_time()
    data = db.extract_data(query, updated, etl_settings.batch_size)
    logger.info(
        f'Выгружено {len(data)} фильмов на основе обновления таблицы {table}')
    return data


def transform(data):
    for row in data:
        doc = {
            "_id": row["id"],
            "id": row["id"],
            "imdb_rating": row["imdb_rating"],
            "genre": row["genre"],
            "title": row["title"],
            "description": row["description"],
            "director": row["director"],
            "actors_names": [row["actors_names"]],
            "writers_names": [row["writers_names"]],
            "actors": row["actors"],
            "writers":  row["writers"],
        }
        yield doc


def load(data):
    successes = 0
    if data:
        elastic = ElasticSearchConnection()
        for ok, action in streaming_bulk(client=elastic.my_connection,
                                         index='again', actions=transform(data)
                                         ):
            successes += ok
            logger.info("Indexed %d documents" % (successes))
        set_time(time_object=data[-1][5])

    else:
        logger.info(
            'Elasticseach в актуальном состоянии, загрузки не требуются')


if __name__ == '__main__':

    my_storage = State(
        JsonFileStorage(file_path=etl_settings.storage_file_path))
    queries_main = {
        'Movies': sql_movies, 'Persons': sql_persons, 'Genres': sql_genres}
    queries_for_check = [sql_movie, sql_person, sql_genre]

    def f():
        logger.info('начало etl')
        db = PostgresConnection()
        Timer(20.0, f).start()
        for query_check, query_main in zip(queries_for_check,
                                           queries_main.items()):
            if check_needs(db, query_check) > get_time():
                logger.info('начало загрузки')
                load(extract(db, query_main[1], query_main[0]))
            else:
                logger.info(
                    f'Elasticseach в актуальном состоянии, обновлений'
                    f'в таблице {query_main[0]} не найдено')
        logger.info('завершение etl')
    f()
