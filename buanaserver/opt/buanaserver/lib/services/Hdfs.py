# -*- encoding: utf 8 -*-

"""
.. module:: main
   :platform: Unix/Linux
   :synopsis: Hadoop main class.
.. moduleauthor::
   :Nickname: Alberto González
   :mail: a.gonzalezmesas@gmail.com
   :Web :
"""

from lib.utils.Actions import Actions
from conf.backup_conf import HADOOP_REMOTE_APP_DIR, HADOOP_REMOTE_SYSTEMD_FILES, \
	HADOOP_LOCAL_APP_DIR, HADOOP_LOCAL_SYSTEMD_FILE, HADOOP_REMOTE_LOGROTATE_FILE, \
	HADOOP_LOCAL_LOGROTATE_FILE

class Hdfs(object):
	"""Hdfs-Backup main methods"""
	def __init__(self):
		super(Hdfs, self).__init__()
		self.HadoopRemoteAppDir = HADOOP_REMOTE_APP_DIR
		self.HadoopRemoteSystemdFiles = HADOOP_REMOTE_SYSTEMD_FILES
		self.HadoopRemoteLogrotateFile = HADOOP_REMOTE_LOGROTATE_FILE
		self.HadoopLocalAppDir = HADOOP_LOCAL_APP_DIR
		self.HadoopLocalSystemdFile = HADOOP_LOCAL_SYSTEMD_FILE
		self.HadoopLocalLogrotateFile = HADOOP_LOCAL_LOGROTATE_FILE
		self.action = Actions()

	def backup(self, RemoteHost):
		Host = RemoteHost
		systemd_stdout = [ ]

		""" Backup: /opt/hadoop """
		home_stdout = self.action.rsync(Host, self.HadoopRemoteAppDir, self.HadoopLocalAppDir)

		""" Backup: /etc/logrotate.d/hadoop """
		logrotateFile_stdout = self.action.rsync(Host, self.HadoopRemoteLogrotateFile, self.HadoopLocalLogrotateFile)

		""" Backup: namenode.service, datanode.service, secondarynamenode.service """
		for systemdFile in self.HadoopRemoteSystemdFiles:
			 stdoutRsync = self.action.rsync(Host, systemdFile, self.HadoopLocalSystemdFile)
			 systemd_stdout.append(stdoutRsync)

		#systemd_stdout_str = str(systemd_stdout)
		logger = '{home_stdout}\n{logrotateFile_stdout}\n{systemd_stdout_str}\n'.format(
				home_stdout=home_stdout,logrotateFile_stdout=logrotateFile_stdout,
				systemd_stdout_str=systemd_stdout)

		return logger
