import get_code_metrics.github_api.post_query as pq
import traceback


class RepositoryInfo:
    def __init__(self, token):
        self.access_token = token

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

        for repository in repository_list:
            repository_info = self.get_repository_info(repository)
            res_all_repository.update({repository: repository_info})

        return res_all_repository
