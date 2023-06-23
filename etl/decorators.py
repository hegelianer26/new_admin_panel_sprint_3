import time
from functools import wraps
from logging import getLogger, StreamHandler


logger = getLogger(__name__)
logger.addHandler(StreamHandler())
logger.setLevel("INFO")


EXECUTION_ERROR = "Произошла ошибка при выполнении функции {name}: {error}."


def backoff(fn):
    @wraps(fn)
    def wrapper(*args, **kw):
        cls = args[0]
        sleep_time = cls.start_sleep_time
        
        while True:
            try:
                return fn(*args, **kw)
            except Exception as error:
                logger.error(EXECUTION_ERROR.format(name=fn.__name__, error=error))
                if sleep_time < cls.border_sleep_time:
                    sleep_time += cls.start_sleep_time * (2**cls.factor)
                else:
                    sleep_time = cls.border_sleep_time
                time.sleep(sleep_time)
                logger.info(sleep_time)

    return wrapper


def reconnect(fn):
    @wraps(fn)
    def wrapper(*args, **kw):
        cls = args[0]

        sleep_time = cls.start_sleep_time
        
        while True:
            print('nj', cls.ping)
                
            if cls.ping == False:
                if sleep_time < cls.border_sleep_time:
                    sleep_time += cls.start_sleep_time * (2**cls.factor)
                else:
                    sleep_time = cls.border_sleep_time
                time.sleep(sleep_time)
                logger.info(sleep_time)

            return fn(*args, **kw)
    return wrapper         
    
            # if cls.ping == False:

            #     if sleep_time < cls.border_sleep_time:
            #         if sleep_time < cls.border_sleep_time:
            #             sleep_time += cls.start_sleep_time * (2**cls.factor)
            #         else:
            #             sleep_time = cls.border_sleep_time
            #         time.sleep(sleep_time)
            #         logger.info(sleep_time)
            #         return fn(*args, **kw)
            # if cls.ping == True:
            #     return fn(*args, **kw)     
     
    #     while True:
                
            # if ping == False:

            #     if sleep_time < cls.border_sleep_time:
            #         sleep_time += cls.start_sleep_time * (2**cls.factor)
            #     else:
            #         sleep_time = cls.border_sleep_time
            #     time.sleep(sleep_time)
            #     logger.info(sleep_time)
            #     print(ping)
            # if ping == True:
            #     return fn(*args, **kw)
    
    # return wrapper 