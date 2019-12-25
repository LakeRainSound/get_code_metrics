import get_code_metrics.cli as cli
import get_code_metrics.cloc.cloc_analyze as cloc
import get_code_metrics.github_api.github_api as ghapi
import get_code_metrics.github_clone.github_clone as ghclone
from pathlib import Path


def main():
    # 引数としてパスを私そのパスが示すfileからリストが返される
    repository_list, output_file_path, clone_path, access_token = cli.command_parser()
    # repository listのrepositoryをcloneする
    print('call clone function and return cloned repositories path')

    # repositoryをcloneする
    print('call cloc analysis function')
    repository_url_list = ghclone.get_github_repository_url_list(repository_list)
    clone = ghclone.GHQ(Path('./ghq'), clone_path)
    clone.clone(repository_url_list)

    # github apiでrepository情報を取得する
    print('call github api(repository info) function')
    repo_info = ghapi.GithubRepositoryInfo(access_token)
    repo_info.get_all_repositories_info(repository_list)

    # github apiでissue情報を取得する
    print('call github api(repository info) function')
    label_info = ghapi.GithubIssueInfo(access_token)
    label_info.get_all_repositories_label_metrics(repository_list)


if __name__ == '__main__':
    main()
