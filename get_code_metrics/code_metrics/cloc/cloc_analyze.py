import subprocess
from pathlib import Path
import re
import json


class Cloc:
    repository_list = []
    path_to_ghq_root = Path('')

    def __init__(self, repository_list, path_to_ghq_root: Path):
        self.repository_list = repository_list
        self.path_to_ghq_root = path_to_ghq_root

    @staticmethod
    def _get_analyzed_cloc(repository_dir):
        return subprocess.Popen(
            ['cloc', '--json', repository_dir],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding='utf-8'
        )

    @staticmethod
    def _is_error(cloc_result_list):
        for cloc_result in cloc_result_list:
            if re.search('error', cloc_result) is not None:
                return True

        return False

    @staticmethod
    def get_cloc_dict(repository_name, cloc_result_list):
        # listが空なら(repositoryに中身がないなら)そのまま返す
        if len(cloc_result_list) == 0:
            return {repository_name: {'cloc': {}}}

        cloc_result_str = ''.join(cloc_result_list)
        cloc_result_json = json.loads(cloc_result_str)

        return {repository_name: {'cloc': cloc_result_json}}

    def get_cloc_results(self):
        res = {}
        for repository_name in self.repository_list:
            # ディレクトリのパスを代入
            repository_dir = str(self.path_to_ghq_root) + '/github.com/' + repository_name

            # processを生成，実行
            cloc_process = self._get_analyzed_cloc(repository_dir)
            while True:
                if cloc_process.poll() is None:
                    cloc_result_list = cloc_process.stdout.readlines()
                    break
            cloc_process.terminate()

            # clocの結果にエラーがあれば以降の処理はせずループの最初に戻る
            if self._is_error(cloc_result_list):
                continue

            # clocの結果をdict化する
            cloc_json = self.get_cloc_dict(repository_name, cloc_result_list)
            res.update(cloc_json)

        cloc_result = {'repository': res}
        return cloc_result