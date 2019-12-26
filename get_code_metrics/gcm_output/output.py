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

    def output_linked_json(self, dict_list, path_to_output_file: Path):
        if len(dict_list) == 0:
            return None

        # 時間情報を結果に書き込む
        self.all_results.update({'datetime': {'start time': self.start_time.isoformat(),
                                              'finish time': self.finish_time.isoformat()}}
                                )

        self.all_results.update({'repository': dict_list[0]})
        for dict_key in dict_list[0].keys():  # type: dict
            for dict_ in dict_list:
                if dict_key in dict_:
                    self.all_results['repository'][dict_key].update(dict_[dict_key])

        with open(str(path_to_output_file), "w") as f:
            json.dump(self.all_results, f, indent=4)


