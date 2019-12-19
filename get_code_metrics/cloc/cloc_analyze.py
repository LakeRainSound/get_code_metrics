import get_code_metrics.config
import subprocess


class Cloc:
    repository_list = []

    def __init__(self, repository_list):
        self.repository_list = repository_list

    @classmethod
    def clone_repository(cls):
        for repository in cls.repository_list:
            print('repository_listをforでまわしてclone')

    @staticmethod
    def analyze_cloc(repository):
        print('repository listのリポジトリに対してcloc(json出力)を実行')

    @classmethod
    def get_cloc_results(cls):
        for repository in cls.repository_list:
            print('analyse_clocを実行')
            print('結果のjsonを出力ファイルに書き込む')
        print('')
