import get_code_metrics.github_api.post_query as pq
from get_code_metrics.gcm_cache.gcm_cache import GCMCache
from pathlib import Path
import traceback
from tqdm import tqdm
import time


class LabelInfo:
    def __init__(self, access_token, use_cache: bool):
        self.access_token = access_token
        self.use_cache = use_cache

    @staticmethod
    def create_issues_info_query(name_with_owner: str, cursor: str):
        query_state = """
                    query{
                      repository(owner: "%s", name: "%s") {
                        issues(first: 100, after: %s, states: CLOSED) {
                          totalCount
                          title_and_label: nodes {
                            title
                            labels{
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
            data_info = pq.post_query(query, self.access_token)

            # repositoryが存在しないならerrorオブジェクトを返す
            if 'errors' in data_info:
                return {'errors': data_info['errors']}

            issues_info = data_info['data']['repository']['issues']

            # 初回はissueの数を入れる
            label_info.setdefault("closedIssueCount", issues_info['totalCount'])

            # title_and_labelリストに追加
            for issue in issues_info['title_and_label']:
                label_info["title_and_label"].append(issue)

            # 最後に続きがあるか判定，cursorに続きを代入
            has_next_page = issues_info['pageInfo']['hasNextPage']
            cursor = issues_info['pageInfo']['endCursor']
            time.sleep(0.75)
            # API制限を回避
            pq.avoid_api_limit(data_info)

        return label_info

    @staticmethod
    def _get_label_metrics(issues):
        label_metrics = {}

        # errorが発生した場合
        if 'errors' in issues:
            return issues

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
        pq.first_avoid_api_limit(self.access_token)

        pbar = tqdm(repository_list,
                    desc="GitHub API(Label Info)",
                    unit="repo")

        print('Start Label Info')
        # キャッシュを取得
        cache_path = Path('./.cache_gcm/.gcm_repo_cache.json').expanduser().resolve()
        gcm_cache = GCMCache(cache_path)
        cache_dict = gcm_cache.get_repository_cache()

        # リポジトリのラベル付与率の取得を開始
        for repository in repository_list:
            try:
                # キャッシュを使う，かつキャッシュにリポジトリが存在している場合
                if self.use_cache and gcm_cache.exist_repository_in_cache(repository, cache_dict):
                    all_repositories_label_metrics[repository] = cache_dict[repository]
                    pbar.update()
                    continue
                # 存在しない場合はそのまま実行
                issues = self.get_issues(repository)
                label_metrics = self._get_label_metrics(issues)
                all_repositories_label_metrics.update({repository: label_metrics})

                # エラーがなければキャッシュに追加
                if not ('errors' in label_metrics.keys()):
                    cache_dict[repository] = label_metrics

            except Exception as e:
                tb = traceback.format_exc(limit=1)
                print('ERROR: {} {}'.format(repository, tb))
                all_repositories_label_metrics.update({repository: pq.get_post_error(e)})
            pbar.update()

        # キャッシュファイルを更新
        gcm_cache.update_repository_cache_file(cache_dict)
        print('Finish Label Info')
        return all_repositories_label_metrics
