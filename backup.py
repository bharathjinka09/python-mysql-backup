import os, subprocess, tarfile
import time, sys
import config
from datetime import datetime

username = config.username
password = config.password
hostname = config.hostname
database = config.database

backup_path = os.getcwd()

class DBBackup:

    def __init__(self):
        self.username = username
        self.password = password
        self.hostname = hostname
        self.database = database
        self.backup_path = backup_path

    def mysql_backup(self):
        backup_date = datetime.now().strftime('%Y%m%d%H%M')
        backup_file = self.database+'_'+backup_date+'.sql'
        dumpfile = open(os.path.join(self.backup_path, backup_file), 'w')
        cmd = ['mysqldump', '--host='+self.hostname, '--user='+self.username, '--password='+self.password, self.database]
        p = subprocess.Popen(cmd, stdout=dumpfile)
        retcode = p.wait()
        dumpfile.close()
        if retcode > 0:
            print('Error:', self.database, 'backup error')
            res = "Error"
        else:
            res = "success"
        self.backup_compress(backup_file)

    def backup_compress(self, backup_file):
        tar_file_path = os.path.join(self.backup_path, backup_file)+'.tar.gz'
        tar = tarfile.open(tar_file_path, 'w:gz')
        tar.add(os.path.join(self.backup_path, backup_file), arcname=backup_file)
        tar.close()
        os.remove(os.path.join(self.backup_path, backup_file))

    def delete_files(self):

        folder_path = os.getcwd()
        file_ends_with = ".sql.tar.gz"
        age_in_days = 10

        if not os.path.exists(folder_path):
            print("Please provide valid path")
            sys.exit(1)
        if os.path.isfile(folder_path):
            print("Please provide directory path")
            sys.exit(2)
        today = datetime.now()
        for each_file in os.listdir(folder_path):
            each_file_path = os.path.join(folder_path,each_file)
            # print(dir(os))

            if os.path.isfile(each_file_path) and each_file_path.endswith(file_ends_with):
                file_creation_date = datetime.fromtimestamp(os.path.getctime(each_file_path))
                # print(today,file_creation_date)
                difference_days = (today-file_creation_date).days
                # print(difference_days)
                if difference_days > age_in_days:
                    os.remove(each_file_path)
                    print("file deleted = ",each_file_path)
                    print(each_file_path,difference_days)
        
                print("No files")


db_backup = DBBackup()
db_backup.mysql_backup()
db_backup.delete_files()
