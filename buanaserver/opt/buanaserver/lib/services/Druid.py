# -*- encoding: utf 8 -*-

"""
.. module:: main
   :platform: Unix/Linux
   :synopsis: Druid main class.
.. moduleauthor::
   :Nickname: Alberto González
   :mail: a.gonzalezmesas@gmail.com
   :Web :
"""

from lib.utils.Actions import Actions
from conf.backup_conf import DRUID_REMOTE_APP_DIR, DRUID_REMOTE_SYSTEMD_FILES, \
	DRUID_LOCAL_APP_DIR, DRUID_LOCAL_SYSTEMD_FILE, DRUID_REMOTE_BINS, \
	DRUID_LOCAL_BINS, DRUID_REMOTE_LOGROTATE, DRUID_LOCAL_LOGROTATE

class Druid(object):
	"""Druid-Backup main methods"""
	def __init__(self):
		super(Druid, self).__init__()
		self.DruidRemoteAppDir = DRUID_REMOTE_APP_DIR
		self.DruidRemoteSystemdFiles = DRUID_REMOTE_SYSTEMD_FILES
		self.DruidRemoteBins = DRUID_REMOTE_BINS
		self.DruidRemoteLogRotate = DRUID_REMOTE_LOGROTATE
		self.DruidLocalAppDir = DRUID_LOCAL_APP_DIR
		self.DruidLocalSystemdFile = DRUID_LOCAL_SYSTEMD_FILE
		self.DruidLocalBins = DRUID_LOCAL_BINS
		self.DruidLocalLogRotate = DRUID_LOCAL_LOGROTATE
		self.action = Actions()

	def backup(self, RemoteHost):
		Host = RemoteHost
		systemd_stdout = [ ]

		""" First Backup: /opt/druid """
		home_stdout = self.action.rsync(Host, self.DruidRemoteAppDir, self.DruidLocalAppDir)

		""" Second Backup: overlord.service, middlemanager.service, historical.service
		broker.service, coordinator.service"""
		for systemdFile in self.DruidRemoteSystemdFiles:
			 stdoutRsync = self.action.rsync(Host, systemdFile, self.DruidLocalSystemdFile)
			 systemd_stdout.append(stdoutRsync)

		""" First Backup: /usr/bin/druid_* """
		hardreload_stdout = self.action.rsync(Host, self.DruidRemoteBins, self.DruidLocalBins)

		""" First Backup: /opt/c_tools/druid_hard_reload """
		logrotate_stdout = self.action.rsync(Host, self.DruidRemoteLogRotate, self.DruidLocalLogRotate)

		logger = '{home_stdout}\n{systemd_stdout_str}\n{hardreload_stdout}\n{logrotate_stdout}\n'.format(
			home_stdout=home_stdout,systemd_stdout_str=systemd_stdout,\
			hardreload_stdout=hardreload_stdout, logrotate_stdout=logrotate_stdout)

		return logger

