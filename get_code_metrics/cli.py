import os.path
import sys
from argparse import ArgumentParser
import re
from pathlib import Path


def command_parser():
    parser = ArgumentParser()
    parser.add_argument('path_to_input_file',
                        type=Path)

    parser.add_argument('-o',
                        '--out',
                        required=True,
                        type=Path,
                        help='path to output file')

    parser.add_argument('--token',
                        '-t',
                        type=str,
                        help='Access Token for GitHub API')

    parser.add_argument('--clone',
                        '-c',
                        type=Path,
                        default='~/.cache/gcm/repositories',
                        help='specify a directory path for cloning repository.')

    parser.add_argument('--force',
                        '-f',
                        action='store_true',
                        help='If not exist specified directory, make it.')

    args = parser.parse_args()

    repository_list = _get_repository_list(args.path_to_input_file)

    # args.outは最後がfile名なのでdirectoryとfile名を分けてdirectoryを渡す
    out_path = args.out  # type: Path
    out_path = out_path.expanduser().resolve()
    _make_directory(out_path.parent)

    # args.cloneはディレクトリなのでそのまま渡す
    clone_path = args.clone  # type: Path
    clone_path = clone_path.expanduser().resolve()
    _make_directory(clone_path)

    access_token = _get_access_token(args.token)

    return repository_list, out_path, clone_path, access_token


def _get_repository_list(path_to_input_file: str):
    repository_list = []
    with open(path_to_input_file, 'r') as f:
        for repository in f:
            # 末尾の改行を削除してリストに追加
            repository = re.sub('[\r\n]+$', '', repository)
            # 最後に空行入れたりしてる場合を排除
            if repository == '' or len(repository) == 0:
                continue
            repository_list.append(repository)

    if not repository_list:
        print('Error: file has no repository list', file=sys.stderr)
        sys.exit(1)

    return repository_list


def _make_directory(path_to_output_dir: Path):
    if path_to_output_dir.exists():
        return

    path_to_output_dir.mkdir(parents=True)
    print('make directory: ', path_to_output_dir)


def _get_access_token(token: str):
    env_token = os.getenv('GCM_GITHUB_TOKEN')
    if token is None or len(token) == 0:
        if env_token is None or len(env_token) == 0:
            print('Error: No GitHub Access Token is specified.', file=sys.stderr)
            exit(1)
        return env_token
    return token
