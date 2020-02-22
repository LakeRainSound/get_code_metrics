import subprocess
from pathlib import Path
from get_code_metrics.gcm_cache.gcm_cache import GCMCache
import json
import re
from tqdm import tqdm


class Cloc:
    def __init__(self, repository_list, path_to_ghq_root: Path, use_cache: bool):
        self.repository_list = repository_list
        self.path_to_ghq_root = path_to_ghq_root
        self.use_cache = use_cache

    @staticmethod
    def _get_analyzed_cloc(repository_dir: Path):
        return subprocess.Popen(
            ['cloc', '--json', '--timeout', '300', str(repository_dir)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding='utf-8'
        )

    @staticmethod
    def _is_error(cloc_result_list):
        for cloc_result in cloc_result_list:
            row = re.compile(r'\d+ error')
            if row.search(cloc_result) is not None:
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

        try:
            cloc_result_json = json.loads(cloc_result_str)
        except Exception as e:
            cloc_result_json = {'errors': [{'message': cloc_result_str}]}

        return cloc_result_json

    def get_cloc_results(self):
        cloc_result = {}
        pbar = tqdm(self.repository_list,
                    desc="CLOC",
                    unit="repo")

        # キャッシュを取得
        cache_path = Path('./.cache_gcm/.gcm_cloc_cache.json').expanduser().resolve()
        gcm_cache = GCMCache(cache_path)
        cache_dict = gcm_cache.get_repository_cache()

        for repository_name in self.repository_list:
            # キャッシュを使う，かつキャッシュにリポジトリが存在している場合
            if self.use_cache and gcm_cache.exist_repository_in_cache(repository_name, cache_dict):
                cloc_result[repository_name] = cache_dict[repository_name]
                pbar.update()
                continue

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
                # エラーがなければキャッシュに追加
                cache_dict[repository_name] = {"cloc": cloc_json}

            cloc_result[repository_name] = {"cloc": cloc_json}
            pbar.update()

        # エラーのないものでキャッシュファイルを更新
        gcm_cache.update_repository_cache_file(cache_dict)
        return cloc_result
