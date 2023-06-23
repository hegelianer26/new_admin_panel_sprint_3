import abc
import json
from json import JSONDecodeError
from pathlib import Path
from typing import Any, Dict

from datetime import datetime


FILE_NOT_FOUND = "Файл {name} не найден. Произошла ошибка: {error}."
READ_ERROR = "Файл {name} не может быть прочитан. Произошла ошибка: {error}."


class BaseStorage:
    @abc.abstractmethod
    def save_state(self, state: Dict) -> None:
        """Сохранить состояние в хранилище"""
        pass

    @abc.abstractmethod
    def retrieve_state(self) -> Dict:
        """Достать состояние из хранилища"""
        pass


class JsonFileStorage(BaseStorage):
    def __init__(self, file_path: str, Path = None):
        self._file_path = file_path

    def save_state(self, state: Dict) -> None:

        with open(self._file_path, "w") as write_file:
            json.dump(state, write_file, ensure_ascii=False)


    def retrieve_state(self) -> Dict:
        state = {}
        with open(self._file_path, "r") as read_file:
            state = json.load(read_file)
        return state

class State:
    def __init__(self, _storage: BaseStorage):
        self._storage = _storage
        self._state = {}

    def set_state(self, key: str, value: Any) -> None:
        """Установить состояние для ключа"""
        if self._state is not None:
            self._state[key] = value
            self._storage.save_state(self._state)

    def get_state(self, key: str) -> Any:
        """Достать состояние ключа"""
        self._state = self._storage.retrieve_state()
        if self._state is None:
            return 9
        return self._state.get(key)


# my_storage = State(JsonFileStorage(file_path='new_admin_panel_sprint_3/etl/states.json'))

