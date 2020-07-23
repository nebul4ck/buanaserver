# -*- encoding: utf 8 -*-

"""
.. module:: main
   :platform: Unix/Linux
   :synopsis: Apache Nifi main class.
.. moduleauthor::
   :Nickname: Alberto González
   :mail: a.gonzalezmesas@gmail.com
   :Web :
"""

from lib.utils.Actions import Actions
from conf.backup_conf import NIFI_REMOTE_CONF_FILES, NIFI_REMOTE_SYSTEMD_FILE,\
	NIFI_REMOTE_FLOW_FILE, NIFI_REMOTE_SSL_TRUSTORE, NIFI_LOCAL_CONF_FILES,\
	NIFI_LOCAL_SYSTEMD_FILE, NIFI_LOCAL_FLOW_FILE, NIFI_LOCAL_SSL_TRUSTORE

class Nifi(object):
	"""Nifi-Backup main methods"""
	def __init__(self):
		super(Nifi, self).__init__()
		self.NifiRemoteConfFiles = NIFI_REMOTE_CONF_FILES
		self.NifiRemoteSystemdFile = NIFI_REMOTE_SYSTEMD_FILE
		self.NifiRemoteFlowFile = NIFI_REMOTE_FLOW_FILE
		self.NifiRemoteSslTrustore = NIFI_REMOTE_SSL_TRUSTORE
		self.NifiLocalConfFiles = NIFI_LOCAL_CONF_FILES
		self.NifiLocalSystemdFile = NIFI_LOCAL_SYSTEMD_FILE
		self.NifiLocalFlowFile = NIFI_LOCAL_FLOW_FILE
		self.NifiLocalSslTrustore = NIFI_LOCAL_SSL_TRUSTORE
		self.action = Actions()

	def backup(self, RemoteHost):
		Host = RemoteHost

		""" Backup: /opt/nifi/conf """
		confFile_stdout = self.action.rsync(Host, self.NifiRemoteConfFiles, self.NifiLocalConfFiles)

		""" Backup: /lib/systemd/system/nifi.service """
		flowfile_stdout = self.action.rsync(Host, self.NifiRemoteFlowFile, self.NifiLocalFlowFile)

		""" Backup: /lib/systemd/system/nifi.service """
		systemd_stdout = self.action.rsync(Host, self.NifiRemoteSystemdFile, self.NifiLocalSystemdFile)

		""" Backup: /opt/nifi/ssl/nificluster_trustore.jks """
		trustore_stdout = self.action.rsync(Host, self.NifiRemoteSslTrustore, self.NifiLocalSslTrustore)

		logger = '{confFile_stdout}\n{flowfile_stdout}\n{systemd_stdout}\n{trustore_stdout}'.format(confFile_stdout=confFile_stdout,
		flowfile_stdout=flowfile_stdout,systemd_stdout=systemd_stdout,trustore_stdout=trustore_stdout)

		return logger
