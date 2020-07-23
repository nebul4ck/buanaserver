# -*- encoding: utf 8 -*-

"""
.. module:: main
   :platform: Unix/Linux
   :synopsis: Curator main class.
.. moduleauthor::
   :Nickname: Alberto González
   :mail: a.gonzalezmesas@gmail.com
   :Web :
"""

from lib.utils.Actions import Actions
from conf.backup_conf import CURATOR_REMOTE_CONF_FILES, CURATOR_REMOTE_CRON_FILES, CURATOR_REMOTE_LOGROTATE_FILE, \
CURATOR_LOCAL_CONF_FILES, CURATOR_LOCAL_CRON_FILES, CURATOR_LOCAL_LOGROTATE_FILES

class Curator(object):
	"""Curator-Backup main methods"""
	def __init__(self):
		super(Curator, self).__init__()
		self.CuratorRemoteConfFiles = CURATOR_REMOTE_CONF_FILES
		self.CuratorRemoteCronFiles = CURATOR_REMOTE_CRON_FILES
		self.CuratorRemoteLogrotateFiles = CURATOR_REMOTE_LOGROTATE_FILE
		self.CuratorLocalConfFiles = CURATOR_LOCAL_CONF_FILES
		self.CuratorLocalCronFiles = CURATOR_LOCAL_CRON_FILES
		self.CuratorLocalLogrotateFiles = CURATOR_LOCAL_LOGROTATE_FILES
        	self.action = Actions()

	def backup(self, RemoteHost):
		Host = RemoteHost

		""" Backup: /opt/elasticsearch-curator/conf/ """
		home_stdout = self.action.rsync(Host, self.CuratorRemoteConfFiles, self.CuratorLocalConfFiles)

		cron_stdout = self.action.rsync(Host, self.CuratorRemoteCronFiles, self.CuratorLocalCronFiles)
		logrotate_stdout = self.action.rsync(Host, self.CuratorRemoteLogrotateFiles, self.CuratorLocalLogrotateFiles)

		logger = '{home_stdout}\n{cron_stdout}\n{logrotate_stdout}\n'.format(
			home_stdout=home_stdout,cron_stdout=cron_stdout,logrotate_stdout=logrotate_stdout)

		return logger
