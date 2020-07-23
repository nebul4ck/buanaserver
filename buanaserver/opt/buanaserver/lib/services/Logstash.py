# -*- encoding: utf 8 -*-

"""
.. module:: main
   :platform: Unix/Linux
   :synopsis: Logstash main class.
.. moduleauthor::
   :Nickname: Alberto González
   :mail: a.gonzalezmesas@gmail.com
   :Web :
"""

from lib.utils.Actions import Actions
from conf.backup_conf import LOGSTASH_REMOTE_CONF_FILES, LOGSTASH_REMOTE_DEFAULT_FILE, \
	LOGSTASH_REMOTE_SYSTEMD_FILE, LOGSTASH_LOCAL_CONF_FILES, LOGSTASH_LOCAL_SYSTEMD_FILE, \
	LOGSTASH_LOCAL_DEFAULT_FILE, LOGSTASH_REMOTE_LOGROTATE_FILE, LOGSTASH_LOCAL_LOGROTATE_FILE

class Logstash(object):
	"""Logstash-Backup main methods"""
	def __init__(self):
		super(Logstash, self).__init__()
		self.LogstashRemoteConfFiles = LOGSTASH_REMOTE_CONF_FILES
		self.LogstashRemoteDefaultFile = LOGSTASH_REMOTE_DEFAULT_FILE
		self.LogstashRemoteSystemdFile = LOGSTASH_REMOTE_SYSTEMD_FILE
		self.LogstashRemoteLogrotateFile = LOGSTASH_REMOTE_LOGROTATE_FILE
		self.LogstashLocalConfFiles = LOGSTASH_LOCAL_CONF_FILES
		self.LogstashLocalSystemdFile = LOGSTASH_LOCAL_SYSTEMD_FILE
		self.LogstashLocalDefaultFile = LOGSTASH_LOCAL_DEFAULT_FILE
		self.LogstashLocalLogrotateFile = LOGSTASH_LOCAL_LOGROTATE_FILE
		self.action = Actions()

	def backup(self, RemoteHost):
		Host = RemoteHost

		""" Backup: /etc/logstash/conf.d/ """
		confFiles_stdout = self.action.rsync(Host, self.LogstashRemoteConfFiles, self.LogstashLocalConfFiles)

		""" Backup: /etc/default/logstash """
		defaultFile_stdout = self.action.rsync(Host, self.LogstashRemoteDefaultFile, self.LogstashLocalDefaultFile)

		""" Backup: /etc/logrotate.d/logstash """
		logrotateFile_stdout = self.action.rsync(Host, self.LogstashRemoteLogrotateFile, self.LogstashLocalLogrotateFile)

		""" Backup: /etc/init.d/logstash """
		systemd_stdout = self.action.rsync(Host, self.LogstashRemoteSystemdFile, \
						self.LogstashLocalSystemdFile)

		logger = '{confFiles_stdout}\n{defaultFile_stdout}\n{logrotateFile_stdout}\n{systemd_stdout}\n'.format(
				confFiles_stdout=confFiles_stdout,defaultFile_stdout=defaultFile_stdout,
				logrotateFile_stdout=logrotateFile_stdout,systemd_stdout=systemd_stdout)

		return logger
