#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
前日24時間分のログを集計して、前日分のサマリログとする
出力ファイル名: ssh_yyyy-mm-dd.json
"""
import sys, os
import re
import json
import datetime
import pathlib
import git

def operate (now:datetime, dir:str):
    """
    対象のファイル一覧を取得する
    """
    logs = []
    target_filename = "ssh_" + (now+datetime.timedelta(days=-1)).strftime('%Y-%m-%d') + "_\d+.json"
    target_jsons = [p for p in dir.iterdir() if p.is_file() and re.search(target_filename, str(p))]
    for target_json in target_jsons:
        with open(target_json, "r") as f:
            log_tmp = json.loads(f.read())
            logs_tmp = log_tmp["logs"]
            for log in logs_tmp:
                logs.append(log)

    j = {"ok": True, "logs":logs}
    return j
    
def main():
    SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
    PJ_DIR = SCRIPT_DIR.parents[0]
    OUTPUT_DIR = pathlib.Path(str(PJ_DIR) + "/docs/api/")

    now = datetime.datetime.now()
    j = operate (now, OUTPUT_DIR)

    OUTPUT_FILE_NAME = "ssh_" + (now+datetime.timedelta(days=-1)).strftime('%Y-%m-%d') + ".json"
    OUTPUT_FILE = pathlib.Path(str(OUTPUT_DIR) + "/" + OUTPUT_FILE_NAME)

    with open(OUTPUT_FILE, mode='w') as f:
        f.write(json.dumps(j, indent=4))

    # commit to git
    git_repo= git.Repo(PJ_DIR)
    git_repo.index.add(str(OUTPUT_FILE))
    commit_message = "[batch] add " + str(OUTPUT_FILE_NAME)
    git_repo.index.commit(commit_message)
    git_repo.remotes.origin.push('HEAD')

if __name__ == '__main__':
  main()

