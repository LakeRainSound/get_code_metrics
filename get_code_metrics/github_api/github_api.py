import get_code_metrics.github_api.repository_info as gh_repo
import get_code_metrics.github_api.label_info as gh_label
import json


def _get_linked_github_api_result(result_list):
    if len(result_list) == 0 or None in result_list:
        return None

    github_results = {}
    github_results.update({'repository': result_list[0]})

    for dict_key in result_list[0].keys():  # type: dict
        for dict_ in result_list:
            if dict_key in dict_:
                github_results['repository'][dict_key].update(dict_[dict_key])

    return github_results


def get_github_api_result(repository_list, access_token):
    result_github_api_list = []

    # github apiでrepository情報を取得する
    repo_info = gh_repo.RepositoryInfo(access_token)
    result_repo_info = repo_info.get_all_repositories_info(repository_list)
    # jsonを結果としてリストに追加
    result_github_api_list.append(result_repo_info)

    # github apiでissue情報を取得する
    label_info = gh_label.LabelInfo(access_token)
    result_label_info = label_info.get_all_repositories_label_metrics(repository_list)
    # jsonを結果としてリストに追加
    result_github_api_list.append(result_label_info)

    result_github_api = _get_linked_github_api_result(result_github_api_list)
    return result_github_api
