# -*- encoding: utf 8 -*-

"""
.. module:: main
   :platform: Unix/Linux
   :synopsis: Rabbitmq main class.
.. moduleauthor::
   :Nickname: Alberto González
   :mail: a.gonzalezmesas@gmail.com
   :Web :
"""

from lib.utils.Actions import Actions
from conf.backup_conf import RABBITMQ_REMOTE_CONFIG_FILE, RABBITMQ_REMOTE_SYSTEMD_FILE, RABBITMQ_REMOTE_LOGROTATE,\
    RABBITMQ_LOCAL_CONFIG_FILE, RABBITMQ_LOCAL_SYSTEMD_FILE, RABBITMQ_LOCAL_LOGROTATE

class Rabbitmq(object):
    """Rabbitmq-Backup main methods"""
    def __init__(self):
        super(Rabbitmq, self).__init__()
        self.RabbitmqRemoteConfFiles = RABBITMQ_REMOTE_CONFIG_FILE
        self.RabbitmqRemoteSystemdFile = RABBITMQ_REMOTE_SYSTEMD_FILE
        self.RabbitmqRemoteLogrotateFile = RABBITMQ_REMOTE_LOGROTATE
        self.RabbitmqLocalConfFiles = RABBITMQ_LOCAL_CONFIG_FILE
        self.RabbitmqLocalSystemdFile = RABBITMQ_LOCAL_SYSTEMD_FILE
        self.RabbitmqLocalLogrotateFile = RABBITMQ_LOCAL_LOGROTATE

        self.action = Actions()

    def backup(self, RemoteHost):
        Host = RemoteHost

        """ Backup: /etc/rabbitmq/ """
        confFile_stdout = self.action.rsync(Host, self.RabbitmqRemoteConfFiles, self.RabbitmqLocalConfFiles)

        """ Backup: /lib/systemd/system/rabbitmq-server.service """
        systemd_stdout = self.action.rsync(Host, self.RabbitmqRemoteSystemdFile, self.RabbitmqLocalSystemdFile)

        """ Backup: /etc/logrotate.d/rabbitmq-server """
        logrotateFile_stdout = self.action.rsync(Host, self.RabbitmqRemoteLogrotateFile, self.RabbitmqLocalLogrotateFile)

        logger = '{confFile_stdout}\n{logrotateFile_stdout}\n{systemd_stdout}\n'.format(
                confFile_stdout=confFile_stdout,logrotateFile_stdout=logrotateFile_stdout,
                systemd_stdout=systemd_stdout)

        return logger
