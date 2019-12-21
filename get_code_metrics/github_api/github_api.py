import requests
import json
import time
# 結果を書き込むための変数を読み込む
import get_code_metrics.config


def post_query(query, access_token):
    headers = {"Authorization": "bearer " + access_token}

    # endpoint
    endpoint = 'https://api.github.com/graphql'
    res = requests.post(endpoint, json=query, headers=headers)
    if res.status_code != 200:
        raise Exception("failed : {}".format(res.status_code))
    return res.json()


class GithubIssueInfo:
    query_issue_state = ''
    access_token = ''

    def __init__(self, access_token):
        self.query_issue_state = """
            query{
              repository(owner: "%s", name: "%s") {
                issues(first: 100, after: %s, states: CLOSED) {
                  totalCount
                  title_and_label: nodes {
                    title
                    labels(first: 20) {
                      label_count: totalCount
                    }
                  }
                  pageInfo{
                    hasNextPage
                    endCursor
                  }
                }
              }
              rateLimit {
                remaining
              }
            }
        """

        self.access_token = access_token

    @classmethod
    def create_issues_info_query(cls, name_with_owner: str, cursor: str):
        query_state = cls.query_issue_state

        # cursorがnullでないなら，つける
        if cursor != 'null':
            cursor = '\"' + cursor + '\"'

        # owner, nameが存在しない場合はNoneをreturn
        if '/' in name_with_owner:
            owner = name_with_owner.split('/')[0]
            name = name_with_owner.split('/')[1]
            query_state = query_state % (owner, name, cursor)
        else:
            return None

        # queryとして送出できる形にする
        res_query = {'query': query_state}
        return res_query

    # print('あるname_with_ownerについて全てのissueとそのラベルを取得')
    @classmethod
    def get_issues(cls, name_with_owner):
        # hasNextPageがfalseになるまで続行, cursorは最初はnull
        has_next_page = True
        cursor = 'null'
        ans = {}
        while has_next_page:
            query = cls.create_issues_info_query(name_with_owner, cursor)
            res_json = post_query(query, cls.access_token)

        return None

    @classmethod
    def calculate_label_metrics(cls, name_with_owner):
        issues = cls.get_issues(name_with_owner)
        print('issueのラベル情報を取得し計算')
        print('計算結果を返す')


class GithubRepositoryInfo:
    query_repository_state = ''
    access_token = ''

    def __init__(self, token):
        self.access_token = token

    @classmethod
    def create_issues_info_query(cls, name_with_owner: str):
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
        query = self.create_issues_info_query(name_with_owner)
        # queryとアクセストークンを渡してpost
        repository_info = post_query(query, self.access_token)

        # 存在しないならNoneを返す
        if 'errors' in repository_info:
            print('ERRORS:', name_with_owner,
                  'doesn\'t exists or has errors. so can\'t get it.')
            return None

        # API制限回避のためrateLimitが1000以下ならsleep
        if repository_info['data']['rateLimit']['remaining'] <= 1000:
            time.sleep(3600)

        return repository_info['data']['repository']

    def get_all_repositories_info(self, repository_list):
        res_all_repository = {}
        for repository in repository_list:
            repository_info = self.get_repository_info(repository)

            # 返り値がNoneなら何もしない
            if repository_info is None:
                continue

            res_all_repository.update({repository: repository_info})

        print(json.dumps(res_all_repository, indent=4))
        return res_all_repository
