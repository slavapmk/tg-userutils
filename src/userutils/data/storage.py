import json
import os.path
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional, Generic, TypeVar

import aiofiles
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Dumpable:
    def to_json(self) -> str:
        pass

    @staticmethod
    def from_json(inp: str, indent: int) -> 'Dumpable':
        pass


T = TypeVar('T', bound=Dumpable)


def check_file_parent(file_path: str):
    dirname = os.path.dirname(file_path)
    if not os.path.exists(dirname):
        os.makedirs(dirname, exist_ok=True)


class StorageFile(Generic[T]):
    def __init__(self, path: str, default_data: T):
        self.path = path
        self.data = default_data

    def save(self) -> None:
        check_file_parent(self.path)
        with open(self.path, 'w') as file:
            file.write(self.data.to_json(indent=2))

    async def async_save(self) -> None:
        check_file_parent(self.path)
        async with aiofiles.open(self.path, 'w') as file:
            await file.write(self.data.to_json(indent=2))

    def from_dict(self, json_data):
        for k, v in json.loads(json_data).items():
            setattr(self.data, k, v)

    def load(self):
        check_file_parent(self.path)
        try:
            with open(self.path, 'r') as file:
                self.from_dict(file.read())
        except IOError:
            self.save()
        except KeyError:
            self.save()

    async def async_load(self):
        check_file_parent(self.path)
        try:
            async with aiofiles.open(self.path, 'r') as file:
                self.from_dict(await file.read())
        except IOError:
            self.save()
        except KeyError:
            self.save()


@dataclass_json
@dataclass
class Config(Dumpable):
    api_id: Optional[str] = field(default=None)
    api_hash: Optional[str] = field(default=None)
    login_phone: Optional[str] = field(default=None)
    login_password: Optional[str] = field(default=None)
    archive_chat: Optional[str] = field(default=None)


config: StorageFile[Config] = StorageFile('storage/config.json', Config())


async def load() -> None:
    config.load()

    if None in [config.data.api_id, config.data.api_hash, config.data.login_phone, config.data.archive_chat]:
        print('Input all queries')
        exit()

#
# # Check required fields
#
# if config.bot_token is None or len(config.bot_token) == 0:
#     config.bot_token = input("Insert your bot token: ")
#     config.save()
