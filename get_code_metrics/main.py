import get_code_metrics.cli as cli
import get_code_metrics.cloc.cloc_analyze as cloc
import get_code_metrics.github_api.github_api as ghapi
import get_code_metrics.github_clone.github_clone as ghclone
import get_code_metrics.gcm_output.output as gcmo
from pathlib import Path
import get_code_metrics.gcm_output.output as gcm_out


def main():
    # start時間を格納
    output_result = gcmo.GCMOUT()
    output_result.set_start_time()

    # 結果のための変数を宣言
    result_json_list = []

    # 引数としてパスを私そのパスが示すfileからリストが返される
    repository_list, path_to_output_file, ghq_root, access_token = cli.command_parser()

    # github apiでrepository情報を取得する
    print('call github api(repository info) function')
    repo_info = ghapi.GithubRepositoryInfo(access_token)
    result_repo_info = repo_info.get_all_repositories_info(repository_list)
    # jsonを結果としてリストに追加
    result_json_list.append(result_repo_info)

    # github apiでissue情報を取得する
    print('call github api(repository info) function')
    label_info = ghapi.GithubIssueInfo(access_token)
    result_label_info = label_info.get_all_repositories_label_metrics(repository_list)
    # jsonを結果としてリストに追加
    result_json_list.append(result_label_info)

    # repositoryをcloneする
    repository_url_list = ghclone.get_github_repository_url_list(repository_list)
    clone = ghclone.GHQ(Path('./ghq'), ghq_root)
    clone.clone(repository_url_list)

    # clocを実行
    cloc_info = cloc.Cloc(repository_list, ghq_root)
    result_cloc = cloc_info.get_cloc_results()
    # jsonを結果としてリストに追加
    result_json_list.append(result_cloc)

    output_result.set_finish_time()
    output_result.output_linked_json(result_json_list, path_to_output_file)


if __name__ == '__main__':
    main()
