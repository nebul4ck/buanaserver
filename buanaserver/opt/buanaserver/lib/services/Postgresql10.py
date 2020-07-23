# -*- encoding: utf 8 -*-

"""
.. module:: main
   :platform: Unix/Linux
   :synopsis: postgresql10 main class.
.. moduleauthor::
   :Nickname: Alberto González
   :mail: a.gonzalezmesas@gmail.com
   :Web :
"""

from lib.utils.Actions import Actions
from conf.backup_conf import POSTGRESQL10_REMOTE_CONFIG_FILE, POSTGRESQL10_REMOTE_HBA_FILE, \
    POSTGRESQL10_LOCAL_CONFIG_FILE, POSTGRESQL10_LOCAL_HBA_FILE

class Postgresql10(object):
    """postgresql10-Backup main methods"""
    def __init__(self):
        super(Postgresql10, self).__init__()
        self.Postgresql10RemoteConfFiles = POSTGRESQL10_REMOTE_CONFIG_FILE
        self.Postgresql10RemoteHbaFile = POSTGRESQL10_REMOTE_HBA_FILE
        self.Postgresql10LocalConfFiles = POSTGRESQL10_LOCAL_CONFIG_FILE
        self.Postgresql10LocalHbaFile = POSTGRESQL10_LOCAL_HBA_FILE

        self.action = Actions()

    def backup(self, RemoteHost):
        Host = RemoteHost

        """ Backup: /etc/postgresql/10/main/posgresql.conf """
        confFile_stdout = self.action.rsync(Host, self.Postgresql10RemoteConfFiles, self.Postgresql10LocalConfFiles)

        """ Backup: /etc/postgresql/10/main/pg_hba.conf """
        hbaFile_stdout = self.action.rsync(Host, self.Postgresql10RemoteHbaFile, self.Postgresql10LocalHbaFile)

        logger = '{confFile_stdout}\n{hbaFile_stdout}\n'.format(
                confFile_stdout=confFile_stdout,hbaFile_stdout=hbaFile_stdout)

        return logger
