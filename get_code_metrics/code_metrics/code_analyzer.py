import get_code_metrics.code_metrics.cloc.cloc_analyze as cloc
import get_code_metrics.code_metrics.github_clone.github_clone as ghclone
from pathlib import Path


def get_code_metrics(repository_list, ghq_root: Path):
    # repositoryをcloneする
    repository_url_list = ghclone.get_github_repository_url_list(repository_list)
    clone = ghclone.GHQ(Path('./ghq'), ghq_root)
    clone.clone(repository_url_list)

    # clocを実行
    cloc_info = cloc.Cloc(repository_list, ghq_root)
    result_cloc = cloc_info.get_cloc_results()

    return result_cloc
