# -*- encoding: utf 8 -*-

"""
.. module:: main
   :platform: Unix/Linux
   :synopsis: Tranquility main class.
.. moduleauthor::
   :Nickname: Alberto González
   :mail: a.gonzalezmesas@gmail.com
   :Web :
"""

from lib.utils.Actions import Actions
from conf.backup_conf import TRANQUILITY_REMOTE_APP_DIR, TRANQUILITY_REMOTE_SYSTEMD_FILE, \
	TRANQUILITY_LOCAL_APP_DIR, TRANQUILITY_LOCAL_SYSTEMD_FILE

class Tranquility(object):
	"""Tranquility-Backup main methods"""
	def __init__(self):
		super(Tranquility, self).__init__()
		self.TranquilityRemoteAppDir = TRANQUILITY_REMOTE_APP_DIR
		self.TranquilityRemoteSystemdFile = TRANQUILITY_REMOTE_SYSTEMD_FILE
		self.TranquilityLocalAppDir = TRANQUILITY_LOCAL_APP_DIR
		self.TranquilityLocalSystemdFile = TRANQUILITY_LOCAL_SYSTEMD_FILE
		self.action = Actions()

	def backup(self, RemoteHost):
		Host = RemoteHost
		systemd_stdout = [ ]

		""" Backup: /opt/tranquility """
		home_stdout = self.action.rsync(Host, self.TranquilityRemoteAppDir, self.TranquilityLocalAppDir)

		""" Backup: tranquility-rt-tasks.service"""
		systemd_stdout = self.action.rsync(Host, self.TranquilityRemoteSystemdFile, \
						self.TranquilityLocalSystemdFile)

		logger = '{home_stdout}\n{systemd_stdout_str}\n'.format(home_stdout=home_stdout,\
					systemd_stdout_str=systemd_stdout)

		return logger
