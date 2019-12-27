import get_code_metrics.cli as cli
import get_code_metrics.cloc.cloc_analyze as cloc
import get_code_metrics.github_api.github_api as ghapi
import get_code_metrics.github_clone.github_clone as ghclone
import get_code_metrics.gcm_output.output as gcmo
from pathlib import Path


def main():
    # start時間を格納
    output_result = gcmo.GCMOUT()
    output_result.set_start_time()

    # 結果のための変数を宣言
    result_json_list = []

    # 引数としてパスを私そのパスが示すfileからリストが返される
    repository_list, path_to_output_file, ghq_root, access_token = cli.command_parser()

    github_api_result = ghapi.get_github_api_result(repository_list, access_token)
    result_json_list.append(github_api_result)

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
