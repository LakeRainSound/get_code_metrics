#!/bin/bash

pipenv run gcm contributor600.txt --out contributor.json
pipenv run gcm fork600.txt --out fork.json
pipenv run gcm dependent600.txt --out dependent.json
pipenv run gcm watcher600.txt --out watcher.json
pipenv run gcm star600.txt --out star.json
