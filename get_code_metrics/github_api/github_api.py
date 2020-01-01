from get_code_metrics.github_api.repository_info import RepositoryInfo
from get_code_metrics.github_api.label_info import LabelInfo
import json


def _get_linked_github_api_result(result_list):
    if len(result_list) == 0 or None in result_list:
        return None

    # key(repository name)を全て取得
    repositories = {}
    for result in result_list:
        repositories = set(repositories) | set(result.keys())

    github_results = {}
    for repo_name in repositories:
        merged = {}
        for result in result_list:
            current_res = result.get(repo_name)
            # 値が無い時はcontinue
            if current_res is None:
                continue
            merged = {**merged, **current_res}
        github_results[repo_name] = merged

    return github_results


def get_github_api_result(repository_list, access_token):
    result_github_api_list = []

    # github apiでrepository情報を取得する
    repo_info = RepositoryInfo(access_token)
    result_repo_info = repo_info.get_all_repositories_info(repository_list)
    # jsonを結果としてリストに追加
    result_github_api_list.append(result_repo_info)

    # github apiでissue情報を取得する
    label_info = LabelInfo(access_token)
    result_label_info = label_info.get_all_repositories_label_metrics(repository_list)
    # jsonを結果としてリストに追加
    result_github_api_list.append(result_label_info)

    # 得られたresult_github_api_listを全てマージしたdictを取得
    result_github_api = _get_linked_github_api_result(result_github_api_list)
    return result_github_api
