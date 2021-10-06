import json
import socket
import urllib.request
import time
import sys
import os
import pipes
dir_path = os.path.dirname(os.path.realpath(__file__))
parameters = sys.argv
if len(parameters) > 1:
    if sys.argv[1] == "debug":
        try:
            settingsFile = open(os.path.join(dir_path, 'settings_debug.json'))
        except:
            print("JSON file is missing")
else:
    try:
        settingsFile = open(os.path.join(dir_path, 'settings.json'))
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
    recursiveMode = True
    backup_path = connection['backup-path']
    filestamp = time.strftime(connection['date-stamp'])
    folder = time.strftime("%Y-%m-%d")

    if isinstance(dbs, str) and dbs == "all-databases":
        recursiveMode = False
    elif not isinstance(dbs, list) and dbs != "all-databases":
        print("Error in settings.json. Value of db is not array nor is it equal to 'all-databases'")
    if backup_path == "":
        backup_path = os.path.join(dir_path, 'backups')
    if recursiveMode:
        for db in dbs:
            final_path = os.path.join(backup_path, folder, host)
            if not os.path.exists(final_path):
                os.makedirs(final_path)
            file_name = final_path+"/"+filestamp + "_" + db + ".sql"
            dumpcmd = "mysqldump -h " + host + " -u " + user + " --password=" + \
                password + " " + db + " --no-tablespaces > " + \
                pipes.quote(file_name)
            os.system(dumpcmd)
            os.system("gzip " + file_name)
    else:
        final_path = os.path.join(backup_path, folder, host)
        if not os.path.exists(final_path):
            os.makedirs(final_path)
        file_name = final_path+"/"+filestamp + "_allDatabases.sql"
        dumpcmd = "mysqldump -h " + host + " -u " + user + " --password=" + \
            password + " --all-databases --no-tablespaces > " + \
            pipes.quote(file_name)
        os.system(dumpcmd)
        os.system("gzip " + file_name)

    if (connection['check-in']):
        try:
            urllib.request.urlopen(
                connection['req-url'], timeout=10)
        except socket.error as e:
            print("Ping failed: %s" % e)
