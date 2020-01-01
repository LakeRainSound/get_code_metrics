import json
import datetime
from pathlib import Path


class GCMOUT:
    all_results = {}
    start_time = None  # type: datetime.datetime
    finish_time = None  # type: datetime.datetime

    def set_start_time(self):
        self.start_time = datetime.datetime.now()

    def set_finish_time(self):
        self.finish_time = datetime.datetime.now()

    def output_linked_json(self, result_list, path_to_output_file: Path):
        if len(result_list) == 0 or None in result_list:
            return None

        # 時間情報を結果に書き込む
        self.all_results.update({'datetime': {'start time': self.start_time.isoformat(),
                                              'finish time': self.finish_time.isoformat()}}
                                )

        self.all_results.setdefault('repository', {})

        # key(repository name)を全て取得
        repositories = {}
        for result in result_list:
            repositories = set(repositories) | set(result.keys())

        for repo_name in repositories:
            merged = {}
            for result in result_list:
                current_res = result.get(repo_name)
                # 値が無い時はcontinue
                if current_res is None:
                    continue
                merged = {**merged, **current_res}
            self.all_results['repository'][repo_name] = merged

        with open(str(path_to_output_file), "w") as f:
            json.dump(self.all_results, f, indent=4)
