from get_code_metrics.cli import command_parser
import get_code_metrics.code_metrics.code_analyzer as code_analyze
from get_code_metrics.github_api.github_api import get_github_api_result
from get_code_metrics.gcm_output.output import GCMOUT
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


def main():
    # start時間を格納
    output_result = GCMOUT()
    output_result.set_start_time()

    # 引数としてパスを私そのパスが示すfileからリストが返される
    repository_list, path_to_output_file, ghq_root, access_token, use_cache = command_parser()

    with ThreadPoolExecutor(max_workers=2, thread_name_prefix='thread') as executor:
        futures = [executor.submit(get_github_api_result,
                                   repository_list,
                                   access_token,
                                   use_cache),
                   executor.submit(code_analyze.get_code_metrics,
                                   repository_list,
                                   ghq_root,
                                   use_cache)
                   ]

    result_list = []
    for future in futures:
        result_list.append(future.result())
    output_result.set_finish_time()
    output_result.output_linked_json(result_list, path_to_output_file)


if __name__ == '__main__':
    main()
