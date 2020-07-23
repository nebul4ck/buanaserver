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
from conf.backup_conf import POSTGRESQLCOMMON_REMOTE_LOGROTATE, POSTGRESQLCOMMON_REMOTE_SYSTEMD_FILE, \
    POSTGRESQLCOMMON_LOCAL_LOGROTATE, POSTGRESQLCOMMON_LOCAL_SYSTEMD_FILE

class Postgresqlcommon(object):
    """postgresql-common-Backup main methods"""
    def __init__(self):
        super(Postgresqlcommon, self).__init__()
        self.PostgresqlcommonRemoteLogrotate = POSTGRESQLCOMMON_REMOTE_LOGROTATE
        self.PostgresqlcommonRemoteSystemdFile = POSTGRESQLCOMMON_REMOTE_SYSTEMD_FILE
        self.PostgresqlcommonLocalLogrotate = POSTGRESQLCOMMON_LOCAL_LOGROTATE
        self.PostgresqlcommonLocalSystemdFile = POSTGRESQLCOMMON_LOCAL_SYSTEMD_FILE

        self.action = Actions()

    def backup(self, RemoteHost):
        Host = RemoteHost

        """ Backup: /etc/logrotate.d/postgresql-common """
        logrotate_stdout = self.action.rsync(Host, self.PostgresqlcommonRemoteLogrotate, self.PostgresqlcommonLocalLogrotate)

        """ Backup: /lib/systemd/system/postgresql* """
        systemdFile_stdout = self.action.rsync(Host, self.PostgresqlcommonRemoteSystemdFile, self.PostgresqlcommonLocalSystemdFile)

        logger = '{logrotate_stdout}\n{systemdFile_stdout}\n'.format(
                logrotate_stdout=logrotate_stdout,systemdFile_stdout=systemdFile_stdout)

        return logger
