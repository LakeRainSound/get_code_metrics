import time
import get_code_metrics.github_api.post_query as post_query


class LabelInfo:
    access_token = ''

    def __init__(self, access_token):
        self.access_token = access_token

    @staticmethod
    def create_issues_info_query(name_with_owner: str, cursor: str):
        query_state = """
                    query{
                      repository(owner: "%s", name: "%s") {
                        issues(first: 100, after: %s, states: CLOSED) {
                          totalCount
                          title_and_label: nodes {
                            title
                            labels(first: 20) {
                              labelCount: totalCount
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

        # cursorがnullでないなら，" "をつける
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

    # あるリポジトリのissueを全て取得
    def get_issues(self, name_with_owner):
        # hasNextPageは1度目の実行のためTrue, cursorは最初はnull
        has_next_page = True
        cursor = 'null'
        label_info = {"title_and_label": []}

        # 全てのissueのラベルデータを取得
        while has_next_page:
            query = self.create_issues_info_query(name_with_owner, cursor)
            data_info = post_query.post_query(query, self.access_token)

            # repositoryが存在しないならNoneを返す
            if 'errors' in data_info:
                print('ERRORS:', name_with_owner,
                      'doesn\'t exists or has errors. so can\'t get it.')
                return None

            issues_info = data_info['data']['repository']['issues']

            # 初回はissueの数を入れる
            label_info.setdefault("closedIssueCount", issues_info['totalCount'])

            # title_and_labelリストに追加
            for issue in issues_info['title_and_label']:
                label_info["title_and_label"].append(issue)

            # 最後に続きがあるか判定，cursorに続きを代入
            has_next_page = issues_info['pageInfo']['hasNextPage']
            cursor = issues_info['pageInfo']['endCursor']

            # API制限を回避
            if data_info['data']['rateLimit']['remaining'] <= 1000:
                time.sleep(3600)

        return label_info

    def get_label_metrics(self, name_with_owner):
        issues = self.get_issues(name_with_owner)

        # errorが発生した場合
        if issues is None:
            return None

        label_metrics = {}
        label_metrics.update({'closedIssueCount': issues['closedIssueCount']})
        has_label_count = 0
        for issue in issues["title_and_label"]:
            if issue['labels']['labelCount'] > 0:
                has_label_count += 1

        label_metrics.update({"hasLabelClosedIssue": has_label_count})

        return label_metrics

    def get_all_repositories_label_metrics(self, repository_list):
        all_repositories_label_metrics = {}

        # APIがはじめに制限にかかりそうならsleepを挟む
        post_query.avoid_api_limit(self.access_token)

        for repository in repository_list:
            label_metrics = self.get_label_metrics(repository)

            all_repositories_label_metrics.update({repository: label_metrics})

        return all_repositories_label_metrics