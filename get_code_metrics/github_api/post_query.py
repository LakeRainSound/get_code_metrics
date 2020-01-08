import time
import requests
import sys
from types import TracebackType
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter


def post_query(query, access_token):
    headers = {"Authorization": "bearer " + access_token}

    # endpoint
    endpoint = 'https://api.github.com/graphql'

    session = requests.Session()
    retries = Retry(total=5,
                    backoff_factor=1,
                    status_forcelist=[500, 502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))
    session.mount('http://', HTTPAdapter(max_retries=retries))

    res = session.post(endpoint, json=query, headers=headers)

    if res.status_code == 403:
        print('ERROR: HTTPS 403')
        time.sleep(3600)
        res = session.post(endpoint, json=query, headers=headers)

    if res.status_code != 200:
        raise Exception("Failed. HTTPS ERROR CODE: {}".format(res.status_code))

    return res.json()


def get_post_error(e: Exception):
    tb = sys.exc_info()[2]  # type: TracebackType
    return {'errors': '{}'.format(e.with_traceback(tb))}


def first_avoid_api_limit(access_token: str):
    query_state = """
                    query{
                      rateLimit {
                        remaining
                      }
                    }
                    """
    try:
        data_info = post_query({'query': query_state}, access_token)
    except Exception as e:
        print('ERROR: first_avoid_api')
        return

    # API制限を回避
    if data_info['data']['rateLimit']['remaining'] <= 1000:
        time.sleep(3600)


def avoid_api_limit(data_info):
    if data_info['data']['rateLimit']['remaining'] <= 1000:
        print('sleep 3600s')
        time.sleep(3600)
