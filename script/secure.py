#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
import re
import json
import datetime
import pathlib
import git
from ipwhois import IPWhois


def targetlines(now:datetime, LOGFILE:pathlib.PosixPath):
    """
    get logs previous 1 hour
    """
    with open (LOGFILE) as f:
        lines = [s.strip() for s in f.readlines()]

    log = []
    date = int((now+datetime.timedelta(hours=-1)).strftime("%-d"))
    if date < 10:
        search_target_time = (now+datetime.timedelta(hours=-1)).strftime("%b  %-d %H")
    else:
        search_target_time = (now+datetime.timedelta(hours=-1)).strftime("%b %-d %H")

    for line in lines:
        if line.find(search_target_time) >= 0:
            log.append(line.split())

    return log

def operate (lines:list, now:datetime):
    """
    ログの内容ごとに抽出する
    """
    logs = []

    now_hour = int(now.strftime("%H"))
    if now_hour == 0:
        date = (now+datetime.timedelta(days=-1)).strftime('%Y-%m-%d')
    else:
        date = now.strftime('%Y-%m-%d')

    tz = "+09:00"
    log_type = "secure"

    for line in lines:
        if "Connection" in line and "closed" in line:
            time = line[2]
            log_type_sub = "Connection closed"
            ip = line[8]
            whois = IPWhois(ip)
            res = whois.lookup_whois()
            country = res['nets'][0]['country']
            log = {"date": date, "time":time, "TZ":tz, "log_type": log_type, "log_type_sub": log_type_sub, "ip": ip, "country": country}
            logs.append(log)

        elif "Invalid" in line and "user" in line:
            time = line[2]
            log_type_sub = "Invalid user"
            user = line[7]
            ip = line[9]
            if ip == "port":
                ip = line[8]
                user = " "
            whois = IPWhois(ip)
            res = whois.lookup_whois()
            country = res['nets'][0]['country']
            log = {"date": date, "time":time, "TZ":tz, "log_type": log_type, "log_type_sub": log_type_sub, "user": user, "ip": ip, "country": country}
            logs.append(log)

        elif "Did" in line and "not" in line and "receive" in line and "identification":
            time = line[2]
            log_type_sub = "Did not receive identification string"
            ip = line[11]
            whois = IPWhois(ip)
            res = whois.lookup_whois()
            country = res['nets'][0]['country']
            log = {"date": date, "time":time, "TZ":tz, "log_type": log_type, "log_type_sub": log_type_sub, "ip": ip, "country": country}
            logs.append(log)

        elif "Accepted" in line and "publickey" in line:
            time = line[2]
            log_type_sub = "Accepted publickey"
            ip = line[10]
            whois = IPWhois(ip)
            res = whois.lookup_whois()
            country = res['nets'][0]['country']
            user = line[8]
            log = {"date": date, "time":time, "TZ":tz, "log_type": log_type, "log_type_sub": log_type_sub, "user": user, "ip": ip, "country": country}
            logs.append(log)

        else:
            pass

    j = {"ok": True, "logs":logs}
    return j

def main():
    LOGFILE = pathlib.Path("/var/log/secure")
    SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
    PJ_DIR = SCRIPT_DIR.parents[0]
    OUTPUT_DIR = pathlib.Path(str(PJ_DIR) + "/docs/api/")

    now = datetime.datetime.now()
    lines = targetlines (now, LOGFILE)
    j = operate (lines, now)

    OUTPUT_FILE_NAME = "secure_" + (now+datetime.timedelta(hours=-1)).strftime('%Y-%m-%d_%H') + ".json"
    OUTPUT_FILE = pathlib.Path(str(OUTPUT_DIR) + "/" + OUTPUT_FILE_NAME)

    with open(OUTPUT_FILE, mode='w') as f:
        f.write(json.dumps(j, indent=4))

    # update metadata.json
    METADATA_FILE_NAME = "metadata.json"
    METADATA_FILE = pathlib.Path(str(OUTPUT_DIR) + "/" + METADATA_FILE_NAME)

    with open(METADATA_FILE, mode="r") as f:
        metadata_json = json.load(f)
    metadata_json['metadata']['secure']['latest'] = OUTPUT_FILE_NAME
    with open(METADATA_FILE, mode="w") as f:
        f.write(json.dumps(metadata_json, indent=4))

    # commit to git
    git_repo= git.Repo(PJ_DIR)

    git_repo.index.add(str(OUTPUT_FILE))
    commit_message = "[batch] add " + str(OUTPUT_FILE_NAME)
    git_repo.index.commit(commit_message)

    git_repo.index.add(str(METADATA_FILE))
    commit_message = "[batch] update " + str(METADATA_FILE)
    git_repo.index.commit(commit_message)

    git_repo.remotes.origin.push('HEAD')

if __name__ == '__main__':
    main()

