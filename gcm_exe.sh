#!/bin/bash

gcm dataset/contributor600.txt --out contributor.json
gcm dataset/fork600.txt --out fork.json
gcm dataset/dependent600.txt --out dependent.json
gcm dataset/watcher600.txt --out watcher.json
gcm dataset/star600.txt --out star.json
