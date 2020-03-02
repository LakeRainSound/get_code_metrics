# get_code_metrics

## Abstract

スラッシュ区切りのGitHubのRepositoryの一覧からissue数，labelの付与率，clocによるLOCのデータが手に入る．

## Environment

- Python >= 3.7

## Usage
example
```shell script
get_code_metrics/main.py path_to_input_file --out path_to_output_file --token GITHUB_ACCSESS_TOKEN
```

### input example
```input.txt
LakeRainSound/get_code_metrics
LakeRainSound/sample-java-project
LakeRainSound/empty
```

### output example
```output.json
{
    "datetime": {
        "start time": "2020-03-02T12:51:59.101732",
        "finish time": "2020-03-02T12:52:05.792194"
    },
    "repository": {
        "LakeRainSound/sample-java-project": {
            "nameWithOwner": "LakeRainSound/sample-java-project",
            "createdAt": "2019-12-14T13:38:40Z",
            "stargazers": {
                "totalCount": 0
            },
            "hasIssuesEnabled": true,
            "isArchived": false,
            "isFork": false,
            "watchers": {
                "totalCount": 1
            },
            "forkCount": 0,
            "isDisabled": false,
            "url": "https://github.com/LakeRainSound/sample-java-project",
            "closedIssueCount": 0,
            "hasLabelClosedIssue": 0,
            "cloc": {
                "header": {
                    "cloc_url": "github.com/AlDanial/cloc",
                    "cloc_version": "1.84",
                    "elapsed_seconds": 0.0150210857391357,
                    "n_files": 1,
                    "n_lines": 3,
                    "files_per_second": 66.5730838214053,
                    "lines_per_second": 199.719251464216
                },
                "Markdown": {
                    "nFiles": 1,
                    "blank": 0,
                    "comment": 0,
                    "code": 3
                },
                "SUM": {
                    "blank": 0,
                    "comment": 0,
                    "code": 3,
                    "nFiles": 1
                }
            }
        },
        "LakeRainSound/empty": {
            "errors": [
                {
                    "type": "NOT_FOUND",
                    "path": [
                        "repository"
                    ],
                    "locations": [
                        {
                            "line": 3,
                            "column": 23
                        }
                    ],
                    "message": "Could not resolve to a Repository with the name 'empty'."
                }
            ],
            "cloc": {}
        },
        "LakeRainSound/get_code_metrics": {
            "nameWithOwner": "LakeRainSound/get_code_metrics",
            "createdAt": "2019-12-18T11:39:49Z",
            "stargazers": {
                "totalCount": 1
            },
            "hasIssuesEnabled": true,
            "isArchived": false,
            "isFork": false,
            "watchers": {
                "totalCount": 1
            },
            "forkCount": 0,
            "isDisabled": false,
            "url": "https://github.com/LakeRainSound/get_code_metrics",
            "closedIssueCount": 6,
            "hasLabelClosedIssue": 5,
            "cloc": {
                "header": {
                    "cloc_url": "github.com/AlDanial/cloc",
                    "cloc_version": "1.84",
                    "elapsed_seconds": 0.0482110977172852,
                    "n_files": 19,
                    "n_lines": 799,
                    "files_per_second": 394.100132534172,
                    "lines_per_second": 16572.9476786739
                },
                "Python": {
                    "nFiles": 11,
                    "blank": 136,
                    "comment": 92,
                    "code": 481
                },
                "XML": {
                    "nFiles": 5,
                    "blank": 0,
                    "comment": 0,
                    "code": 35
                },
                "Dockerfile": {
                    "nFiles": 1,
                    "blank": 6,
                    "comment": 0,
                    "code": 23
                },
                "Markdown": {
                    "nFiles": 1,
                    "blank": 8,
                    "comment": 0,
                    "code": 11
                },
                "Bourne Shell": {
                    "nFiles": 1,
                    "blank": 1,
                    "comment": 0,
                    "code": 6
                },
                "SUM": {
                    "blank": 151,
                    "comment": 92,
                    "code": 556,
                    "nFiles": 19
                }
            }
        }
    }
}
```

### option
`--clone (-c)`
You can specify Path to clone Repos.
Default is '~/.cache/gcm/repositories'

`--token (-t)`
You can specify GitHub Access Token.
If you don't use this option, get_code_metrics uses $GCM_GITHUB_TOKEN. If $GCM_GITHUB_TOKEN doesn't also exist, it will error.

`--no-cache`
If repositories information which you want to get exist in cache file, get_code_metrics uses cache by default.

`--no-cache` option disable using cache. 


## Author

LakeRainSound

## LICENCE
MIT