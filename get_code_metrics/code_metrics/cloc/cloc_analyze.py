import subprocess
from pathlib import Path
import json


class Cloc:
    def __init__(self, repository_list, path_to_ghq_root: Path):
        self.repository_list = repository_list
        self.path_to_ghq_root = path_to_ghq_root

    @staticmethod
    def _get_analyzed_cloc(repository_dir: Path):
        return subprocess.Popen(
            ['cloc', '--json', str(repository_dir)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding='utf-8'
        )

    @staticmethod
    def _is_error(cloc_result_list):
        for cloc_result in cloc_result_list:
            if 'Unable to read:' in cloc_result:
                return True

        return False

    @staticmethod
    def _get_error_massage(cloc_result_list):
        cloc_result_str = ''.join(cloc_result_list)
        return {'errors': [{'message': cloc_result_str}]}

    @staticmethod
    def get_cloc_dict(cloc_result_list):
        # listが空なら(repositoryに中身がないなら)そのまま返す
        if len(cloc_result_list) == 0:
            return {}

        cloc_result_str = ''.join(cloc_result_list)
        cloc_result_json = json.loads(cloc_result_str)

        return cloc_result_json

    def get_cloc_results(self):
        cloc_result = {}
        for repository_name in self.repository_list:
            # ディレクトリのパスを代入
            repository_dir = self.path_to_ghq_root / 'github.com' / repository_name

            # processを生成，実行
            cloc_process = self._get_analyzed_cloc(repository_dir)
            while True:
                if cloc_process.poll() is None:
                    cloc_result_list = cloc_process.stdout.readlines()
                    break
            cloc_process.terminate()

            # clocの結果にエラーがあればエラーメッセージを記録
            if self._is_error(cloc_result_list):
                cloc_json = self._get_error_massage(cloc_result_list)
            else:
                cloc_json = self.get_cloc_dict(cloc_result_list)
            cloc_result[repository_name] = {"cloc": cloc_json}

        return cloc_result
