import json

import get_code_metrics.github_api.post_query as pq
from pathlib import Path
from get_code_metrics.gcm_cache.gcm_cache import GCMCache
import traceback
from tqdm import tqdm


class RepositoryInfo:
    def __init__(self, token: str, use_cache: bool):
        self.access_token = token
        self.use_cache = use_cache  # type: bool

    @staticmethod
    def create_repository_info_query(name_with_owner: str):
        query_state = """
        query{
          repository(owner: "%s", name: "%s") {
            nameWithOwner
            createdAt
            stargazers {
              totalCount
            }
            hasIssuesEnabled
            isArchived
            isFork
            forkCount
            isDisabled
            url
          }
          rateLimit {
            remaining
          }
        }
        """

        # owner, nameが存在しない場合はNoneをreturn
        if '/' in name_with_owner:
            owner = name_with_owner.split('/')[0]
            name = name_with_owner.split('/')[1]
            query_state = query_state % (owner, name)
        else:
            return None

        # queryとして送出できる形にする
        res_query = {'query': query_state}
        return res_query

    def get_repository_info(self, name_with_owner):
        # queryを作成
        query = self.create_repository_info_query(name_with_owner)
        # queryとアクセストークンを渡してpost
        try:
            repository_info = pq.post_query(query, self.access_token)
            print(json.dumps(repository_info, indent=4))
        except Exception as e:
            tb = traceback.format_exc(limit=1)
            print('ERROR: {} {}'.format(name_with_owner, tb))
            return pq.get_post_error(e)

        # repositoryが存在しないならerrorオブジェクトを返す
        if 'errors' in repository_info:
            return {'errors': repository_info['errors']}

        # API制限回避のためrateLimitが1000以下ならsleep
        pq.avoid_api_limit(repository_info)

        return repository_info['data']['repository']

    def get_all_repositories_info(self, repository_list):
        res_all_repository = {}

        # APIがはじめに制限にかかりそうならsleepを挟む
        pq.first_avoid_api_limit(self.access_token)

        pbar = tqdm(repository_list,
                    desc="GitHub API(Repo Info)",
                    unit="repo")

        print('Start Repo Info')
        # キャッシュを取得
        cache_path = Path('./.cache_gcm/.gcm_label_cache.json').expanduser().resolve()
        gcm_cache = GCMCache(cache_path)
        cache_dict = gcm_cache.get_repository_cache()

        # Repository Infoの取得開始
        for repository in repository_list:
            # キャッシュを使う，かつキャッシュにリポジトリが存在している場合
            if self.use_cache and gcm_cache.exist_repository_in_cache(repository, cache_dict):
                res_all_repository[repository] = cache_dict[repository]
                pbar.update()
                continue

            repository_info = self.get_repository_info(repository)
            res_all_repository.update({repository: repository_info})
            # エラーがなければキャッシュに追加
            if not ('errors' in repository_info.keys()):
                cache_dict[repository] = repository_info
            pbar.update()

        # キャッシュファイルを更新
        gcm_cache.update_repository_cache_file(cache_dict)
        print('Finish Repo Info')
        print(json.dumps(res_all_repository, indent=4))
        return res_all_repository
