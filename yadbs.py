import json
import socket
import urllib.request
import time
import sys
import os
import pipes
parameters = sys.argv
if len(parameters) > 1:
    if sys.argv[1] == "debug":
        try:
            settingsFile = open(r'./settings_debug.json')
        except:
            print("JSON file is missing")
    else:
        try:
            settingsFile = open(r'./settings.json')
        except:
            print("JSON file is missing")
    try:
        settings = json.load(settingsFile)
    except:
        print("Error in json file")
connections = settings['database']

for connection in connections:

    host = connection['host']
    user = connection['user']
    password = connection['password']
    dbs = connection['db']
    backup_path = connection['backup-path']
    filestamp = time.strftime(connection['data-stamp'])
    folder = time.strftime("%Y-%m-%d")

    if backup_path == "":
        backup_path = "./backups/"
    else:
        if not os.path.exists(backup_path):
            os.mkdir(backup_path)

    final_path = os.path.join(backup_path, folder)
    if not os.path.exists(final_path):
        os.mkdir(final_path)
    for db in dbs:
        file_name = final_path+"/"+filestamp + "_" + db + ".sql"
        dumpcmd = "mysqldump -h " + host + " -u " + user + " --password=" + \
            password + " " + db + " --no-tablespaces > " + \
            pipes.quote(file_name)
        os.system(dumpcmd)
        os.system("gzip " + file_name)

    if (connection['check-in']):
        try:
            urllib.request.urlopen(
                connection['req-url'], timeout=10)
        except socket.error as e:
            print("Ping failed: %s" % e)
