# -*- encoding: utf 8 -*-

"""
.. module:: main
   :platform: Unix/Linux
   :synopsis: Spark main class.
.. moduleauthor::
   :Nickname: Alberto González
   :mail: a.gonzalezmesas@gmail.com
   :Web :
"""

from lib.utils.Actions import Actions
from conf.backup_conf import SPARK_REMOTE_APP_DIR, SPARK_REMOTE_SYSTEMD_FILES, \
	SPARK_LOCAL_APP_DIR, SPARK_LOCAL_SYSTEMD_FILE, SPARK_REMOTE_LOGROTATE, \
	SPARK_LOCAL_LOGROTATE

class Spark(object):
	"""Spark-Backup main methods"""
	def __init__(self):
		super(Spark, self).__init__()
		self.SparkRemoteAppDir = SPARK_REMOTE_APP_DIR
		self.SparkRemoteSystemdFiles = SPARK_REMOTE_SYSTEMD_FILES
		self.SparkRemoteLogRotate = SPARK_REMOTE_LOGROTATE
		self.SparkLocalAppDir = SPARK_LOCAL_APP_DIR
		self.SparkLocalSystemdFile = SPARK_LOCAL_SYSTEMD_FILE
		self.SparkLocalLogRotate = SPARK_LOCAL_LOGROTATE
		self.action = Actions()

	def backup(self, RemoteHost):
		Host = RemoteHost
		systemd_stdout = [ ]

		""" First Backup: /opt/spark """
		home_stdout = self.action.rsync(Host, self.SparkRemoteAppDir, self.SparkLocalAppDir)

		""" Second Backup: spark-master.service, spark-worker.service """
		for systemdFile in self.SparkRemoteSystemdFiles:
			 stdoutRsync = self.action.rsync(Host, systemdFile, self.SparkLocalSystemdFile)
			 systemd_stdout.append(stdoutRsync)

		""" Third Backup: /opt/spark """
		logrotate_stdout = self.action.rsync(Host, self.SparkRemoteLogRotate, self.SparkLocalLogRotate)

		logger = '{home_stdout}\n{systemd_stdout_str}\n'.format(home_stdout=home_stdout,\
					systemd_stdout_str=systemd_stdout, logrotate_stdout=logrotate_stdout)

		return logger
