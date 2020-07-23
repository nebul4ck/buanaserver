# -*- encoding: utf 8 -*-

"""
.. module:: main
   :platform: Unix/Linux
   :synopsis: VerneMQ main class.
.. moduleauthor::
   :Nickname: Alberto González
   :mail: a.gonzalezmesas@gmail.com
   :Web :
"""

from lib.utils.Actions import Actions
from conf.backup_conf import VERNEMQ_REMOTE_CONF_FILES, VERNEMQ_REMOTE_SYSTEMD_FILE, \
	VERNEMQ_LOCAL_CONF_FILES, VERNEMQ_LOCAL_SYSTEMD_FILE, VERNEMQ_REMOTE_STORE, \
	VERNEMQ_REMOTE_INITD, VERNEMQ_REMOTE_SHARE, VERNEMQ_LOCAL_STORE, VERNEMQ_LOCAL_INITD, \
	VERNEMQ_LOCAL_SHARE
	#VERNEMQ_REMOTE_LOGROTATE_FILE, VERNEMQ_LOCAL_LOGROTATE_FILE

class Vernemq(object):
	"""Vernemq-Backup main methods"""
	def __init__(self):
		super(Vernemq, self).__init__()
		self.VernemqRemoteConfFiles = VERNEMQ_REMOTE_CONF_FILES
		self.VernemqRemoteSystemdFile = VERNEMQ_REMOTE_SYSTEMD_FILE
		self.VernemqRemoteStore = VERNEMQ_REMOTE_STORE
		self.VernemqRemoteInitd = VERNEMQ_REMOTE_INITD
		self.VernemqRemoteShare = VERNEMQ_REMOTE_SHARE
		self.VernemqLocalConfFiles = VERNEMQ_LOCAL_CONF_FILES
		self.VernemqLocalSystemdFile = VERNEMQ_LOCAL_SYSTEMD_FILE
		self.VernemqLocalStore = VERNEMQ_LOCAL_STORE
		self.VernemqLocalInitd = VERNEMQ_LOCAL_INITD
		self.VernemqLocalShare = VERNEMQ_LOCAL_SHARE
		self.action = Actions()

	def backup(self, RemoteHost):
		Host = RemoteHost

		""" Backup: /etc/vernemq/ """
		confFile_stdout = self.action.rsync(Host, self.VernemqRemoteConfFiles, self.VernemqLocalConfFiles)

		#""" Backup: /etc/logrotate.d/vernemq """
		#logrotateFile_stdout = rsync(Host, self.VernemqRemoteLogrotateFile, self.VernemqLocalLogrotateFile)

		""" Backup: /lib/systemd/system/vernemq.service """

		systemd_stdout = self.action.rsync(Host, self.VernemqRemoteSystemdFile, self.VernemqLocalSystemdFile)

		#logger = '{confFile_stdout}\n{logrotateFile_stdout}\n{systemd_stdout}\n'.format(
		#		confFile_stdout=confFile_stdout,logrotateFile_stdout=logrotateFile_stdout,
		#		systemd_stdout=systemd_stdout)

		""" Backup: /opt/store/vernemq """

		store_stdout = self.action.rsync(Host, self.VernemqRemoteStore, self.VernemqLocalStore)

		""" Backup: /etc/initd.d/vernemq """

		initd_stdout = self.action.rsync(Host, self.VernemqRemoteInitd, self.VernemqLocalInitd)

		""" Backup: /usr/share/vernemq """

		share_stdout = self.action.rsync(Host, self.VernemqRemoteShare, self.VernemqLocalShare)

		logger = '{confFile_stdout}\n{systemd_stdout}\n{store_stdout}\n{initd_stdout}\n{share_stdout}'.format(
				confFile_stdout=confFile_stdout,systemd_stdout=systemd_stdout,
				store_stdout=store_stdout,initd_stdout=initd_stdout,share_stdout=share_stdout)

		return logger
