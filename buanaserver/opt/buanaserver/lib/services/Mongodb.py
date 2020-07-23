# -*- encoding: utf 8 -*-

"""
.. module:: main
   :platform: Unix/Linux
   :synopsis: Mongodb main class.
.. moduleauthor::
   :Nickname: Alberto González
   :mail: a.gonzalezmesas@gmail.com
   :Web :
"""

from lib.utils.Actions import Actions
from conf.backup_conf import MONGODB_REMOTE_CONFIG_FILE, MONGODB_REMOTE_SYSTEMD_FILE, MONGODB_REMOTE_LOGROTATE,\
    MONGODB_LOCAL_CONFIG_FILE, MONGODB_LOCAL_SYSTEMD_FILE, MONGODB_LOCAL_LOGROTATE

class Mongodb(object):
    """Mongodb-Backup main methods"""
    def __init__(self):
        super(Mongodb, self).__init__()
        self.MongodbRemoteConfFiles = MONGODB_REMOTE_CONFIG_FILE
        self.MongodbRemoteSystemdFile = MONGODB_REMOTE_SYSTEMD_FILE
        self.MongodbRemoteLogrotateFile = MONGODB_REMOTE_LOGROTATE
        self.MongodbLocalConfFiles = MONGODB_LOCAL_CONFIG_FILE
        self.MongodbLocalSystemdFile = MONGODB_LOCAL_SYSTEMD_FILE
        self.MongodbLocalLogrotateFile = MONGODB_LOCAL_LOGROTATE

        self.action = Actions()

    def backup(self, RemoteHost):
        Host = RemoteHost

        """ Backup: /etc/mongod.conf """
        confFile_stdout = self.action.rsync(Host, self.MongodbRemoteConfFiles, self.MongodbLocalConfFiles)

        """ Backup: /lib/systemd/system/mongod.service """
        systemd_stdout = self.action.rsync(Host, self.MongodbRemoteSystemdFile, self.MongodbLocalSystemdFile)

        """ Backup: /etc/logrotate.d/mongodb-server """
        logrotateFile_stdout = self.action.rsync(Host, self.MongodbRemoteLogrotateFile, self.MongodbLocalLogrotateFile)

        logger = '{confFile_stdout}\n{logrotateFile_stdout}\n{systemd_stdout}\n'.format(
                confFile_stdout=confFile_stdout,logrotateFile_stdout=logrotateFile_stdout,
                systemd_stdout=systemd_stdout)

        return logger
