import json
from json import JSONDecodeError
from pathlib import Path


class GCMCache:
    def __init__(self, path_to_cache_file: Path):
        self.path_to_cache_file = path_to_cache_file

    def _create_repository_cache_file(self):
        init_dict = {}
        with open(str(self.path_to_cache_file), 'w') as f:
            json.dump(init_dict, f)

    def get_repository_cache(self):
        # 存在しないなら作成する
        if not self.path_to_cache_file.exists():
            self._create_repository_cache_file()

        with open(str(self.path_to_cache_file), 'r') as f:
            try:
                repository_cache = json.load(f)
            except JSONDecodeError:
                repository_cache = {}
        return repository_cache

    @staticmethod
    def exist_repository_in_cache(key_name: str, cache_dict: dict):
        if key_name in cache_dict.keys():
            return True
        return False

    @staticmethod
    def get_updated_repository_cache_dict(cache_dict: dict, result):
        cache_dict.update(result)
        return cache_dict

    def update_repository_cache_file(self, updated_dict: dict):
        with open(str(self.path_to_cache_file), 'w') as f:
            json.dump(updated_dict, f, indent=4)
