import os.path
import sys
from argparse import ArgumentParser


def command_parser():
    parser = ArgumentParser()
    print('parseした結果(入力ファイルと出力ファイルを返す)')
    parser.add_argument('path_to_input_file',
                        type=str)
    parser.add_argument('-o',
                        '--out',
                        type=str,
                        default='./result.json')
    parser.add_argument('--force',
                        '-f',
                        action='store_true',
                        help='If not exist specified directory, make it.')

    args = parser.parse_args()

    repository_list = get_repository_list(args.path_to_input_file)
    check_directory_exist(args.out, args.force)

    return repository_list, args.out


def get_repository_list(path_to_input_file: str):
    repository_list = []
    print('repository listがあるなら返す，ないならエラーで終了')
    with open(path_to_input_file, 'r') as f:
        for repository in f:
            repository_list.append(repository)

    if not repository_list:
        print('Error: file has no repository list', file=sys.stderr)
        sys.exit(1)

    return repository_list


def check_directory_exist(path_to_output_file: str, create_force: bool):
    directory_path = os.path.split(path_to_output_file)[0]

    # コマンドの指定でdirectory pathが存在し，directory pathが実行時の環境に存在せず
    # かつforceフラグが立っている場合
    if directory_path and not os.path.exists(directory_path) and create_force:
        print('make directory! ', directory_path)
        os.makedirs(directory_path, exist_ok=True)
        return

    # コマンドの指定でdirectory pathが存在するがdirectory pathが実行時の環境に存在せず
    # かつforceフラグが立っていない場合
    if not os.path.exists(directory_path) and not create_force:
        print('Error: specified directory does not exit', file=sys.stderr)
        sys.exit(1)
