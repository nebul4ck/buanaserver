# -*- encoding: utf 8 -*-

"""
.. module:: main
   :platform: Unix/Linux
   :synopsis: Apache Nifi-Registry main class.
.. moduleauthor::
   :Nickname: Alberto González
   :mail: a.gonzalezmesas@gmail.com
   :Web :
"""

from lib.utils.Actions import Actions
from conf.backup_conf import NIFI_REGISTRY_REMOTE_CONF_FILES, NIFI_REGISTRY_REMOTE_SYSTEMD_FILE,\
	NIFI_REGISTRY_REMOTE_SSL_TRUSTORE, NIFI_REGISTRY_LOCAL_CONF_FILES,\
	NIFI_REGISTRY_LOCAL_SSL_TRUSTORE, NIFI_REGISTRY_LOCAL_SYSTEMD_FILE

class Nifiregistry(object):
	"""NifiRegistry-Backup main methods"""
	def __init__(self):
		super(Nifiregistry, self).__init__()
		self.NifiregistryRemoteConfFiles = NIFI_REGISTRY_REMOTE_CONF_FILES
		self.NifiregistryRemoteSystemdFile = NIFI_REGISTRY_REMOTE_SYSTEMD_FILE
		self.NifiregistryRemoteSslTrustore = NIFI_REGISTRY_REMOTE_SSL_TRUSTORE
		self.NifiregistryLocalConfFiles = NIFI_REGISTRY_LOCAL_CONF_FILES
		self.NifiregistryLocalSslTrustore = NIFI_REGISTRY_LOCAL_SSL_TRUSTORE
		self.NifiregistryLocalSystemdFile = NIFI_REGISTRY_LOCAL_SYSTEMD_FILE
		self.action = Actions()

	def backup(self, RemoteHost):
		Host = RemoteHost

		""" Backup: /opt/nifi-registry/conf """
		confFile_stdout = self.action.rsync(Host, self.NifiregistryRemoteConfFiles, self.NifiregistryLocalConfFiles)

		""" Backup: /lib/systemd/system/nifi-registry.service """
		systemd_stdout = self.action.rsync(Host, self.NifiregistryRemoteSystemdFile, self.NifiregistryLocalSystemdFile)

		""" Backup: /opt/nifi-registry/ssl/nificluster_trustore.jks """
		trustore_stdout = self.action.rsync(Host, self.NifiregistryRemoteSslTrustore, self.NifiregistryLocalSslTrustore)

		logger = '{confFile_stdout}\n{systemd_stdout}\n{trustore_stdout}'.format(confFile_stdout=confFile_stdout,
			systemd_stdout=systemd_stdout, trustore_stdout=trustore_stdout)

		return logger
