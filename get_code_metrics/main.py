import get_code_metrics.cli as cli
import get_code_metrics.cloc.cloc_analyze as cloc
import get_code_metrics.github_api.github_api as ghapi


def main():
    # 引数としてパスを私そのパスが示すfileからリストが返される
    repository_list, output_file_path, clone_path, access_token = cli.command_parser()
    # repository listのrepositoryをcloneする
    print('call clone function and return cloned repositories path')

    # cloneしたrepositoryをclocで分析した結果を返す
    print('call cloc analysis function')
    cloc_obj = cloc.Cloc(repository_list)
    # 必要なrepository_listをclone
    cloc_obj.clone_repository()
    #
    cloc_obj.get_cloc_results()

    # github apiでrepository情報を取得する
    print('call github api(repository info) function')
    repo_info = ghapi.GithubRepositoryInfo(access_token)
    repo_info.get_all_repositories_info(repository_list)

    # github apiでissue情報を取得する
    print('call github api(repository info) function')


if __name__ == '__main__':
    main()
