# -*- encoding: utf 8 -*-

"""
.. module:: main
   :platform: Unix/Linux
   :synopsis: Zookeeper main class.
.. moduleauthor::
   :Nickname: Alberto González
   :mail: a.gonzalezmesas@gmail.com
   :Web :
"""

from lib.utils.Actions import Actions
from conf.backup_conf import ZOOKEEPER_REMOTE_APP_DIR, ZOOKEEPER_REMOTE_SYSTEMD_FILE, \
	ZOOKEEPER_LOCAL_APP_DIR, ZOOKEEPER_LOCAL_SYSTEMD_FILE, ZOOKEEPER_REMOTE_LOGROTATE, \
	ZOOKEEPER_LOCAL_LOGROTATE

class Zookeeper(object):
	"""Zookeeper-Backup main methods"""
	def __init__(self):
		super(Zookeeper, self).__init__()
		self.ZookeeperRemoteAppDir = ZOOKEEPER_REMOTE_APP_DIR
		self.ZookeeperRemoteSystemdFile = ZOOKEEPER_REMOTE_SYSTEMD_FILE
		self.ZookeeperRemoteLogRotate = ZOOKEEPER_REMOTE_LOGROTATE
		self.ZookeeperLocalAppDir = ZOOKEEPER_LOCAL_APP_DIR
		self.ZookeeperLocalSystemdFile = ZOOKEEPER_LOCAL_SYSTEMD_FILE
		self.ZookeeperLocalLogRotate = ZOOKEEPER_LOCAL_LOGROTATE
		self.action = Actions()

	def backup(self, RemoteHost):
		Host = RemoteHost

		""" First Backup: /opt/zookeeper """
		home_stdout = self.action.rsync(Host, self.ZookeeperRemoteAppDir, self.ZookeeperLocalAppDir)

		""" Second Backup: zookeeper.service """
		systemd_stdout = self.action.rsync(Host, self.ZookeeperRemoteSystemdFile, \
						self.ZookeeperLocalSystemdFile)

		""" Second Backup: zookeeper.service """
		logrotate_stdout = self.action.rsync(Host, self.ZookeeperRemoteLogRotate, \
						self.ZookeeperLocalLogRotate)

		logger = '{home_stdout}\n{systemd_stdout}\n{logrotate_stdout}\n'.format(home_stdout=home_stdout,\
					systemd_stdout=systemd_stdout, logrotate_stdout=logrotate_stdout)

		return logger
