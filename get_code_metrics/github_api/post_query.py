import time
import requests


def post_query(query, access_token):
    headers = {"Authorization": "bearer " + access_token}

    # endpoint
    endpoint = 'https://api.github.com/graphql'
    res = requests.post(endpoint, json=query, headers=headers)
    if res.status_code != 200:
        raise Exception("failed : {}".format(res.status_code))
    return res.json()


def first_avoid_api_limit(access_token: str):
    query_state = """
                    query{
                      rateLimit {
                        remaining
                      }
                    }
                    """
    data_info = post_query({'query': query_state}, access_token)
    # API制限を回避
    if data_info['data']['rateLimit']['remaining'] <= 1000:
        time.sleep(3600)


def avoid_api_limit(data_info):
    if data_info['data']['rateLimit']['remaining'] <= 1000:
        time.sleep(3600)
