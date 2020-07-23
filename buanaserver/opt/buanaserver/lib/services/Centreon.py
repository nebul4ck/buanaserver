# -*- encoding: utf 8 -*-

"""
.. module:: main
   :platform: Unix/Linux
   :synopsis: Centreon main class.
.. moduleauthor::
   :Nickname: Alberto González
   :mail: a.gonzalezmesas@gmail.com
   :Web :
"""

import os

from lib.utils.Actions import Actions
from conf.backup_conf import CENTREON_REMOTE_CONF_FILE, CENTREON_LOCAL_CONF_FILE

class Centreon(object):
	"""Centreon-Backup main methods"""
	def __init__(self):
		super(Centreon, self).__init__()
		self.CentreonRemoteConfFile = CENTREON_REMOTE_CONF_FILE
		self.CentreonLocalConfFile = CENTREON_LOCAL_CONF_FILE
		self.action = Actions()

	def backup(self, RemoteHost):
		Host = RemoteHost

		""" First Backup: /usr/local/nagios/etc/nrpe.cfg """

		CentreonLocalHostnameConfFile = '{CentreonLocalConfFile}/{host}'.format(host=Host,
						CentreonLocalConfFile=self.CentreonLocalConfFile)

		if not os.path.isdir(CentreonLocalHostnameConfFile):
			os.mkdir(CentreonLocalHostnameConfFile)
			home_stdout = self.action.rsync(Host, self.CentreonRemoteConfFile, CentreonLocalHostnameConfFile)
		else:
			home_stdout = self.action.rsync(Host, self.CentreonRemoteConfFile, CentreonLocalHostnameConfFile)

		logger = home_stdout

		return logger
