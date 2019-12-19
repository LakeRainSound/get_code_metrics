import requests
import json
# 結果を書き込むための変数を読み込む
import get_code_metrics.config

# access token
token = 'hoge'
# endpoint
endpoint = 'https://api.github.com/graphql'


def post_query(query):
    headers = {"Authorization": "bearer " + token}
    res = requests.post(endpoint, json=query, headers=headers)
    if res.status_code != 200:
        raise Exception("failed : {}".format(res.status_code))
    return res.json()


class GithubIssueInfo:
    query_issue_state = ''

    def __init__(self):
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

    @classmethod
    def create_issues_info_query(cls, owner: str, name: str, cursor: str):
        query_state = cls.query_issue_state

        # cursorが存在しないならnullを代入
        if cursor is None:
            cursor = 'null'
        else:
            cursor = '\"' + cursor + '\"'

        # owner, nameが存在しない場合はNoneをreturn
        if owner is None or name is None:
            return None
        else:
            query_state = query_state % (owner, name, cursor)

        # queryとして送出できる形にする
        res_query = {'query': query_state}
        return res_query

    @staticmethod
    def get_issues(name_with_owner):
        # hasNextPageがfalseになるまで続行
        print('あるname_with_ownerについて全てのissueとそのラベルを取得')
        return None

    @classmethod
    def calculate_label_metrics(cls, name_with_owner):
        issues = cls.get_issues(name_with_owner)
        print('issueのラベル情報を取得し計算')
        print('計算結果を返す')



class GithubRepositoryInfo:
    query_repository_state = ''

    def __init__(self):
        self.query_repository_state = """
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

    @classmethod
    def create_issues_info_query(cls, owner: str, name: str, cursor: str):
        query_state = cls.query_repository_state

        # cursorが存在しないならnullを代入
        if cursor is None:
            cursor = 'null'
        else:
            cursor = '\"' + cursor + '\"'
        # owner, nameが存在しない場合はNoneをreturn
        if owner is None or name is None:
            return None
        else:
            query_state = query_state % (owner, name, cursor)

        # queryとして送出できる形にする
        res_query = {'query': query_state}
        return res_query

    @staticmethod
    def get_repository_info(name_with_owner):
        # 存在しないならNoneを返す
        print('repositroyの情報を出力')
        return None
