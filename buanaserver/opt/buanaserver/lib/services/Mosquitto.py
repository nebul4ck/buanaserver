# -*- encoding: utf 8 -*-

"""
.. module:: main
   :platform: Unix/Linux
   :synopsis: Mosquitto main class.
.. moduleauthor::
   :Nickname: Alberto González
   :mail: a.gonzalezmesas@gmail.com
   :Web :
"""

from lib.utils.Actions import Actions
from conf.backup_conf import MOSQUITTO_REMOTE_CONFIG_FILE, MOSQUITTO_REMOTE_SYSTEMD_FILE, MOSQUITTO_REMOTE_LOGROTATE,\
    MOSQUITTO_REMOTE_CONFIG_DIR, MOSQUITTO_LOCAL_CONFIG_FILE, MOSQUITTO_LOCAL_SYSTEMD_FILE, MOSQUITTO_LOCAL_LOGROTATE,\
    MOSQUITTO_LOCAL_CONFIG_DIR

class Mosquitto(object):
    """Mosquitto-Backup main methods"""
    def __init__(self):
        super(Mosquitto, self).__init__()
        self.MosquittoRemoteConfFiles = MOSQUITTO_REMOTE_CONFIG_FILE
        self.MosquittoRemoteConfDir = MOSQUITTO_REMOTE_CONFIG_DIR
        self.MosquittoRemoteSystemdFile = MOSQUITTO_REMOTE_SYSTEMD_FILE
        self.MosquittoRemoteLogrotateFile = MOSQUITTO_REMOTE_LOGROTATE
        self.MosquittoLocalConfFiles = MOSQUITTO_LOCAL_CONFIG_FILE
        self.MosquittoLocalConfDir = MOSQUITTO_LOCAL_CONFIG_DIR
        self.MosquittoLocalSystemdFile = MOSQUITTO_LOCAL_SYSTEMD_FILE
        self.MosquittoLocalLogrotateFile = MOSQUITTO_LOCAL_LOGROTATE

        self.action = Actions()

    def backup(self, RemoteHost):
        Host = RemoteHost

        """ Backup: /etc/mosquitto/mosquitto.conf """
        confFile_stdout = self.action.rsync(Host, self.MosquittoRemoteConfFiles, self.MosquittoLocalConfFiles)

        """ Backup: /etc/mosquitto/conf.d """
        confDir_stdout = self.action.rsync(Host, self.MosquittoRemoteConfDir, self.MosquittoLocalConfDir)

        """ Backup: /lib/systemd/system/mosquitto.service """
        systemd_stdout = self.action.rsync(Host, self.MosquittoRemoteSystemdFile, self.MosquittoLocalSystemdFile)

        """ Backup: /etc/logrotate.d/mosquitto """
        logrotateFile_stdout = self.action.rsync(Host, self.MosquittoRemoteLogrotateFile, self.MosquittoLocalLogrotateFile)

        logger = '{confFile_stdout}\n{confDir_stdout}\n{logrotateFile_stdout}\n{systemd_stdout}\n'.format(
                confFile_stdout=confFile_stdout,confDir_stdout=confDir_stdout, logrotateFile_stdout=logrotateFile_stdout,
                systemd_stdout=systemd_stdout)

        return logger
