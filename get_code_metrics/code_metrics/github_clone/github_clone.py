import subprocess
import platform
import logging
import time
import zipfile
import shutil
import os
from pathlib import Path
from typing import TYPE_CHECKING

import requests
from tqdm import tqdm

if TYPE_CHECKING:
    from typing import List

logger = logging.getLogger(__name__)
ghq_revision = "v0.12.6"
ghq_dl_url_base = "https://github.com/motemen/ghq/releases/download/"


def _download_ghq_binary(dest: 'Path'):
    if not dest.exists():
        dest.mkdir(parents=True)
    machine_arch = "amd64" if platform.machine() == "x86_64" else "386"
    os_type = platform.system().lower()
    dl_url_path = "{version}/ghq_{os}_{arch}.zip".format(version=ghq_revision,
                                                         os=os_type,
                                                         arch=machine_arch)
    ghq_zip = dest / dl_url_path.split("/")[-1]
    if not ghq_zip.exists():
        resp = requests.get(ghq_dl_url_base + dl_url_path)
        with ghq_zip.open('wb') as f:
            f.write(resp.content)
    if not (ghq_zip.parent / ghq_zip.stem).exists():
        with zipfile.ZipFile(str(ghq_zip)) as zip_archive:
            zip_archive.extractall(str(ghq_zip.parent))
    ghq_unarchived = ghq_zip.parent / ghq_zip.stem / "ghq"
    ghq_bin = ghq_zip.parent / "ghq"  # type: Path
    shutil.move(str(ghq_unarchived), str(ghq_bin))
    ghq_bin.chmod(0o755)
    return ghq_bin


def get_github_repository_url_list(repository_list):
    repository_url_list = list(map(lambda x: 'https://github.com/' + x, repository_list))
    return repository_url_list


class GHQ(object):
    N_JOBS = 6
    INTERVAL = 5

    # Commands
    CLONE_CMD = "import"
    LIST_CMD = "list"

    def __init__(self, ghq_binary: 'Path', clone_dest: 'Path'):
        if not ghq_binary.is_absolute():
            ghq_binary = ghq_binary.expanduser().resolve()
        if not ghq_binary.exists():
            ghq_binary = _download_ghq_binary(ghq_binary.parent)
        self.ghq = ghq_binary
        self.dest = clone_dest
        self._options = {
            self.CLONE_CMD: ["-u", "-P"],
            self.LIST_CMD: ["-p"]
        }

    def set_options(self, command: str, args: 'List[str]'):
        self._options[command] = args

    def get_options(self, command: str) -> 'List[str]':
        opts = self._options.get(command)
        if opts is not None:
            return opts
        return []

    def _get_ghq_process(self, command: str):
        env_vars = os.environ
        return subprocess.Popen(
            [str(self.ghq), command, *self.get_options(command)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=env_vars.update({"GHQ_ROOT": str(self.dest)}),
            encoding='utf-8',
        )

    def clone(self, repositories: 'List[str]'):
        steps = range(0, len(repositories), self.N_JOBS)
        logger.info("Start to clone")
        ghq_process = None
        try:
            pbar = tqdm(steps, total=len(repositories), desc="Cloned Repos", unit="repo")
            for i in steps:
                # Spawn ghq process every time
                ghq_process = self._get_ghq_process(self.CLONE_CMD)
                to_dl = repositories[i:i+self.N_JOBS]
                # Append '\n' as suffix
                to_dl = list(map(lambda x: x + '\n', to_dl))
                ghq_process.stdin.writelines(to_dl)
                ghq_process.stdin.close()
                while True:
                    line = ghq_process.stdout.readline()
                    logger.debug(line)
                    if ghq_process.poll() is not None:
                        break
                ghq_process.terminate()
                pbar.update(len(to_dl))
                time.sleep(self.INTERVAL)
        except Exception as e:
            logger.exception(str(e))
            logger.error("KILL ghq process")
        finally:
            if ghq_process is not None:
                ghq_process.terminate()
                ghq_process.wait(60)
            logger.error("Cloning Done")
        return self.list()

    def list(self) -> 'List[str]':
        ghq_process = self._get_ghq_process(self.LIST_CMD)
        try:
            stdout, _ = ghq_process.communicate()
            return stdout.split("\n")
        except Exception as e:
            logger.error(e)
            return []
        finally:
            ghq_process.terminate()
            ghq_process.wait()
