
import psycopg2
from logging import getLogger, StreamHandler
from decorators import backoff
import psycopg2.extras
from configs import postgres_settings, etl_settings

logger = getLogger(__name__)
logger.addHandler(StreamHandler())
logger.setLevel("INFO")


class PostgresConnection:
    start_sleep_time = etl_settings.start_sleep_time
    factor = etl_settings.factor
    border_sleep_time = etl_settings.border_sleep_time

    def __init__(self):
        self.my_connection = None
        self.my_cursor = None
        self.params = None
        self._connect()

    @backoff
    def _connect(self):
        self.my_connection = psycopg2.connect(**postgres_settings.dict())
        self.my_cursor = self.my_connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)
        logger.info("Подключились к postgres")

    @backoff
    def extract_data(self, sql_statement, updated, size):
        self.my_cursor.execute(sql_statement.format(updated))
        result = self.my_cursor.fetchmany(size=size)
        if result:
            return result
        return None

    @backoff
    def __del__(self):
        for c in (self.my_cursor, self.my_connection):
            try:
                c.close()
            except:
                pass
        logger.info("Закрыли соединение c postgres и курсор ")


# my_storage = State(JsonFileStorage(file_path=etl_settings.storage_file_path))


# def get_time():
#     time_dirty = my_storage.get_state("Movies")
#     time = datetime.strptime(time_dirty, "%Y-%m-%d %H:%M:%S.%f%z")
#     print(time)
#     return time


# def set_time(time_object):
#     dt_str = time_object.strftime("%Y-%m-%d %H:%M:%S.%f%z")
#     print('что не сохраняет', dt_str)
#     my_storage.set_state('Movies', dt_str)

# db = PostgresConnection()
# q = db.extract_data(sql_persons, get_time(), 990)
# r = db.extract_data(sql_genres, get_time(), 1)
# n = db.extract_data(sql_genres, get_time(), 1)

# set_time(n[-1][5])

# def set_time(time_object):
#     dt_str = time_object.strftime("%Y-%m-%d %H:%M:%S.%f%z")
#     my_storage.set_state('Movies', dt_str)


# def check_needs(db):
#     updated = get_time(movies='Genres')
#     data = db.extract_data(sql_movie, updated, 1)
#     for i in data:
#         print(i[0])
#         return i[0]

# queires = [sql_movies, sql_persons, sql_genres]

# def extract(db):
#     updated = get_time(movies='Genres')
#     for query in queires:
#         data = db.extract_data(query, updated, 1)
#         print('______________')
#         print (data)

# extract(db)
