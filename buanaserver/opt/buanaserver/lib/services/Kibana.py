# -*- encoding: utf 8 -*-

"""
.. module:: main
   :platform: Unix/Linux
   :synopsis: Kibana main class.
.. moduleauthor::
   :Nickname: Alberto González
   :mail: a.gonzalezmesas@gmail.com
   :Web :
"""

from lib.utils.Actions import Actions
from conf.backup_conf import KIBANA_REMOTE_CONF_FILE, KIBANA_REMOTE_DEFAULT_FILE, \
	KIBANA_REMOTE_SYSTEMD_FILE, KIBANA_LOCAL_CONF_FILE, KIBANA_LOCAL_SYSTEMD_FILE, \
	KIBANA_LOCAL_DEFAULT_FILE, KIBANA_REMOTE_LOGROTATE_FILE, KIBANA_LOCAL_LOGROTATE_FILE, \
	KIBANA_REMOTE_INIT_FILE, KIBANA_LOCAL_INIT_FILE

class Kibana(object):
	"""Kibana-Backup main methods"""
	def __init__(self):
		super(Kibana, self).__init__()
		self.KibanaRemoteConfFile = KIBANA_REMOTE_CONF_FILE
		self.KibanaRemoteDefaultFile = KIBANA_REMOTE_DEFAULT_FILE
		self.KibanaRemoteLogrotateFile = KIBANA_REMOTE_LOGROTATE_FILE
		self.KibanaRemoteSystemdFile = KIBANA_REMOTE_SYSTEMD_FILE
		self.KibanaRemoteInitFile = KIBANA_REMOTE_INIT_FILE
		self.KibanaLocalConfFile = KIBANA_LOCAL_CONF_FILE
		self.KibanaLocalSystemdFile = KIBANA_LOCAL_SYSTEMD_FILE
		self.KibanaLocalInitFile = KIBANA_LOCAL_INIT_FILE
		self.KibanaLocalDefaultFile = KIBANA_LOCAL_DEFAULT_FILE
		self.KibanaLocalLogrotateFile = KIBANA_LOCAL_LOGROTATE_FILE
		self.action = Actions()

	def backup(self, RemoteHost):
		Host = RemoteHost

		""" Backup: /etc/kibana/kibana.yml """
		confFile_stdout = self.action.rsync(Host, self.KibanaRemoteConfFile, self.KibanaLocalConfFile)

		""" Backup: /etc/default/kibana """
		defaultFile_stdout = self.action.rsync(Host, self.KibanaRemoteDefaultFile, self.KibanaLocalDefaultFile)

		""" Backup: /etc/logrotate.d/kibana """
		logrotateFile_stdout = self.action.rsync(Host, self.KibanaRemoteLogrotateFile, self.KibanaLocalLogrotateFile)

		""" Backup: /etc/init.d/kibana """

		systemd_stdout = self.action.rsync(Host, self.KibanaRemoteSystemdFile, \
						self.KibanaLocalSystemdFile)

		init_stdout = self.action.rsync(Host, self.KibanaRemoteInitFile, \
						self.KibanaLocalInitFile)

		logger = '{confFile_stdout}\n{defaultFile_stdout}\n{logrotateFile_stdout}\n{systemd_stdout}\n{init_stdout}\n'.format(
				confFile_stdout=confFile_stdout,logrotateFile_stdout=logrotateFile_stdout,
				defaultFile_stdout=defaultFile_stdout,systemd_stdout=systemd_stdout,init_stdout=init_stdout)

		return logger
