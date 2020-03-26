import os, subprocess, tarfile
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

db_backup = DBBackup()
db_backup.mysql_backup()
