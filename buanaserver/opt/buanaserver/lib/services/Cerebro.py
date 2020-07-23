# -*- encoding: utf 8 -*-

"""
.. module:: main
   :platform: Unix/Linux
   :synopsis: Cerebro main class.
.. moduleauthor::
   :Nickname: Alberto González
   :mail: a.gonzalezmesas@gmail.com
   :Web :
"""

from lib.utils.Actions import Actions
from conf.backup_conf import CEREBRO_REMOTE_APP_DIR, CEREBRO_REMOTE_SYSTEMD_FILE, \
	CEREBRO_LOCAL_APP_DIR, CEREBRO_LOCAL_SYSTEMD_FILE, CEREBRO_REMOTE_LOGROTATE, \
	CEREBRO_LOCAL_LOGROTATE

class Cerebro(object):
	"""Cerebro-Backup main methods"""
	def __init__(self):
		super(Cerebro, self).__init__()
		self.CerebroRemoteAppDir = CEREBRO_REMOTE_APP_DIR
		self.CerebroRemoteSystemdFile = CEREBRO_REMOTE_SYSTEMD_FILE
		self.CerebroRemoteLogRotate = CEREBRO_REMOTE_LOGROTATE
		self.CerebroLocalAppDir = CEREBRO_LOCAL_APP_DIR
		self.CerebroLocalSystemdFile = CEREBRO_LOCAL_SYSTEMD_FILE
		self.CerebroLocalLogRotate = CEREBRO_LOCAL_LOGROTATE
		self.action = Actions()

	def backup(self, RemoteHost):
		Host = RemoteHost

		""" First Backup: /opt/cerebro """
		home_stdout = self.action.rsync(Host, self.CerebroRemoteAppDir, self.CerebroLocalAppDir)

		""" Second Backup: Cerebro.service """
		systemd_stdout = self.action.rsync(Host, self.CerebroRemoteSystemdFile, \
						self.CerebroLocalSystemdFile)

		logrotate_stdout = self.action.rsync(Host, self.CerebroRemoteLogRotate, \
						self.CerebroLocalLogRotate)

		logger = '{home_stdout}\n{systemd_stdout}\n{logrotate_stdout}\n'.format(home_stdout=home_stdout,\
					systemd_stdout=systemd_stdout, logrotate_stdout=logrotate_stdout)

		return logger
