# -*- encoding: utf 8 -*-

"""
.. module:: main
   :platform: Unix/Linux
   :synopsis: Kaa main class.
.. moduleauthor::
   :Nickname: Alberto González
   :mail: a.gonzalezmesas@gmail.com
   :Web :
"""

from lib.utils.Actions import Actions
from conf.backup_conf import KAA_REMOTE_FILES, KAA_REMOTE_DEFAULT_FILE, \
	KAA_REMOTE_SYSTEMD_FILE, KAA_LOCAL_FILES, KAA_LOCAL_SYSTEMD_FILE, \
	KAA_LOCAL_DEFAULT_FILE

class Kaa(object):
	"""Kaa-Backup main methods"""
	def __init__(self):
		super(Kaa, self).__init__()
		self.KaaRemoteFiles = KAA_REMOTE_FILES
		self.KaaRemoteDefaultFile = KAA_REMOTE_DEFAULT_FILE
		self.KaaRemoteSystemdFile = KAA_REMOTE_SYSTEMD_FILE
		self.KaaLocalFiles = KAA_LOCAL_FILES
		self.KaaLocalSystemdFile = KAA_LOCAL_SYSTEMD_FILE
		self.KaaLocalDefaultFile = KAA_LOCAL_DEFAULT_FILE
		self.action = Actions()

	def backup(self, RemoteHost):
		Host = RemoteHost

		""" Backup: /usr/lib/kaa-node/conf/ """
		confFiles_stdout = self.action.rsync(Host, self.KaaRemoteFiles, self.KaaLocalFiles)

		""" Backup: /etc/default/kaa-node """
		defaultFile_stdout = self.action.rsync(Host, self.KaaRemoteDefaultFile, self.KaaLocalDefaultFile)

		""" Backup: /lib/systemd/system/kaa.service """

		systemd_stdout = self.action.rsync(Host, self.KaaRemoteSystemdFile, \
						self.KaaLocalSystemdFile)

		logger = '{confFiles_stdout}\n{defaultFile_stdout}\n{systemd_stdout}\n'.format(confFiles_stdout=confFiles_stdout,\
					defaultFile_stdout=defaultFile_stdout,systemd_stdout=systemd_stdout)

		return logger
