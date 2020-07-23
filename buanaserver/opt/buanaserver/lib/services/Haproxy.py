# -*- encoding: utf 8 -*-

"""
.. module:: main
   :platform: Unix/Linux
   :synopsis: HAproxy main class.
.. moduleauthor::
   :Nickname: Alberto González
   :mail: a.gonzalezmesas@gmail.com
   :Web :
"""

from lib.utils.Actions import Actions
from conf.backup_conf import HAPROXY_REMOTE_CONF_FILES, HAPROXY_REMOTE_DEFAULT_FILE, \
	HAPROXY_REMOTE_SYSTEMD_FILE, HAPROXY_LOCAL_CONF_FILES, HAPROXY_LOCAL_SYSTEMD_FILE, \
	HAPROXY_LOCAL_DEFAULT_FILE, HAPROXY_REMOTE_LOGROTATE_FILE, HAPROXY_LOCAL_LOGROTATE_FILE, \
	HAPROXY_REMOTE_RSYSLOG, HAPROXY_LOCAL_RSYSLOG

class Haproxy(object):
	"""HAproxy-Backup main methods"""
	def __init__(self):
		super(Haproxy, self).__init__()
		self.HaproxyRemoteConfFiles = HAPROXY_REMOTE_CONF_FILES
		self.HaproxyRemoteDefaultFile = HAPROXY_REMOTE_DEFAULT_FILE
		self.HaproxyRemoteLogrotateFile = HAPROXY_REMOTE_LOGROTATE_FILE
		self.HaproxyRemoteSystemdFile = HAPROXY_REMOTE_SYSTEMD_FILE
		self.HaproxyRemoteRsyslogFile = HAPROXY_REMOTE_RSYSLOG
		self.HaproxyLocalConfFiles = HAPROXY_LOCAL_CONF_FILES
		self.HaproxyLocalSystemdFile = HAPROXY_LOCAL_SYSTEMD_FILE
		self.HaproxyLocalDefaultFile = HAPROXY_LOCAL_DEFAULT_FILE
		self.HaproxyLocalLogrotateFile = HAPROXY_LOCAL_LOGROTATE_FILE
		self.HaproxyLocalRsyslogFile = HAPROXY_LOCAL_RSYSLOG
		self.action = Actions()

	def backup(self, RemoteHost):
		Host = RemoteHost

		""" Backup: /etc/haproxy/ """
		confFile_stdout = self.action.rsync(Host, self.HaproxyRemoteConfFiles, self.HaproxyLocalConfFiles)

		""" Backup: /etc/default/haproxy """
		defaultFile_stdout = self.action.rsync(Host, self.HaproxyRemoteDefaultFile, self.HaproxyLocalDefaultFile)

		""" Backup: /etc/logrotate.d/haproxy """
		logrotateFile_stdout = self.action.rsync(Host, self.HaproxyRemoteLogrotateFile, self.HaproxyLocalLogrotateFile)

		""" Backup: /lib/systemd/system/haproxy.service """

		systemd_stdout = self.action.rsync(Host, self.HaproxyRemoteSystemdFile, self.HaproxyLocalSystemdFile)

		""" Backup: /etc/rsyslog.d/49-haproxy.conf """
		rsyslog_stdout = self.action.rsync(Host, self.HaproxyRemoteRsyslogFile, self.HaproxyLocalRsyslogFile)

		logger = '{confFile_stdout}\n{defaultFile_stdout}\n{logrotateFile_stdout}\n{systemd_stdout}\n{rsyslog_stdout}\n'.format(
				confFile_stdout=confFile_stdout,logrotateFile_stdout=logrotateFile_stdout,
				defaultFile_stdout=defaultFile_stdout,systemd_stdout=systemd_stdout,rsyslog_stdout=rsyslog_stdout)

		return logger
