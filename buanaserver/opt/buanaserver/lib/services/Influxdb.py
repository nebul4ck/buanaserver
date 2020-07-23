# -*- encoding: utf 8 -*-

"""
.. module:: main
   :platform: Unix/Linux
   :synopsis: Influxdb main class.
.. moduleauthor::
   :Nickname: Alberto González
   :mail: a.gonzalezmesas@gmail.com
   :Web :
"""

from lib.utils.Actions import Actions
from conf.backup_conf import INFLUXDB_REMOTE_CONFIG_FILE, INFLUXDB_REMOTE_SYSTEMD_FILE, INFLUXDB_REMOTE_LOGROTATE,\
    INFLUXDB_REMOTE_RSYSLOG, INFLUXDB_LOCAL_CONFIG_FILE, INFLUXDB_LOCAL_SYSTEMD_FILE, INFLUXDB_LOCAL_LOGROTATE, \
    INFLUXDB_LOCAL_RSYSLOG

class Influxdb(object):
    """Influxdb-Backup main methods"""
    def __init__(self):
        super(Influxdb, self).__init__()
        self.InfluxdbRemoteConfFiles = INFLUXDB_REMOTE_CONFIG_FILE
        self.InfluxdbRemoteSystemdFile = INFLUXDB_REMOTE_SYSTEMD_FILE
        self.InfluxdbRemoteLogrotateFile = INFLUXDB_REMOTE_LOGROTATE
        self.InfluxdbRemoteRsyslogFile = INFLUXDB_REMOTE_RSYSLOG
        self.InfluxdbLocalConfFiles = INFLUXDB_LOCAL_CONFIG_FILE
        self.InfluxdbLocalSystemdFile = INFLUXDB_LOCAL_SYSTEMD_FILE
        self.InfluxdbLocalLogrotateFile = INFLUXDB_LOCAL_LOGROTATE
        self.InfluxdbLocalRsyslogFile = INFLUXDB_LOCAL_RSYSLOG

        self.action = Actions()

    def backup(self, RemoteHost):
        Host = RemoteHost

        """ Backup: /etc/influxdb.conf """
        confFile_stdout = self.action.rsync(Host, self.InfluxdbRemoteConfFiles, self.InfluxdbLocalConfFiles)

        """ Backup: /lib/systemd/system/influxdb.service """
        systemd_stdout = self.action.rsync(Host, self.InfluxdbRemoteSystemdFile, self.InfluxdbLocalSystemdFile)

        """ Backup: /etc/logrotate.d/influxdb """
        logrotateFile_stdout = self.action.rsync(Host, self.InfluxdbRemoteLogrotateFile, self.InfluxdbLocalLogrotateFile)

        """ Backup: /etc/rsyslog.d/49-influxdb.conf """
        rsyslogFile_stdout = self.action.rsync(Host, self.InfluxdbRemoteRsyslogFile, self.InfluxdbLocalRsyslogFile)

        logger = '{confFile_stdout}\n{logrotateFile_stdout}\n{systemd_stdout}\n{rsyslogFile_stdout}\n'.format(
                confFile_stdout=confFile_stdout,logrotateFile_stdout=logrotateFile_stdout,
                systemd_stdout=systemd_stdout, rsyslogFile_stdout=rsyslogFile_stdout)

        return logger
